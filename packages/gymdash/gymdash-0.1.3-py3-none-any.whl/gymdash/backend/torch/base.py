import os
import pathlib
from abc import abstractmethod, ABC
from collections import OrderedDict
from typing import Any, Dict, Union

from torch.nn.modules import Module

from gymdash.backend.torch.utils import get_available_accelerator
from gymdash.backend.core.simulation.callbacks import (BaseCustomCallback,
                                                       EmptyCallback)
from gymdash.backend.core.simulation.base import StopSimException

try:
    import torch
    import torch.nn as nn
    from torch.nn.modules.loss import _Loss
    from torch.optim import Optimizer
    from torch.utils.data import DataLoader
    from torch.utils.tensorboard.writer import SummaryWriter
    from torchvision import datasets
    from torchvision.transforms import ToTensor
    _has_torch = True
except ImportError:
    _has_torch = False

if not _has_torch:
    raise ImportError("Install pytorch to use base gymdash-pytorch utilities.")

class InferenceModel(ABC):
    @abstractmethod
    def produce(self, inputs):
        pass

class SimulationMLModel():
    def __init__(self, model: nn.Module) -> None:
        self.model = model
        self.train_kwargs = {}
        self.val_kwargs = {}
        self.test_kwargs = {}
        self.inference_kwargs = {}

        self._is_training = False
        self._is_validating = False
        self._is_testing = False
        self._is_inferring = False

    @property
    def is_busy(self):
        return \
            self._is_training   or \
            self._is_validating or \
            self._is_testing    or \
            self._is_inferring

    def forward(self, x):
        return self.model.forward(x)
    
    def set_model(self, new_model: nn.Module):
        self.model = new_model

    @abstractmethod
    def _train(self, **kwargs):
        pass
    @abstractmethod
    def _validate(self, **kwargs):
        pass
    @abstractmethod
    def _test(self, **kwargs):
        pass
    
    def train(self, **kwargs):
        self._is_training = True
        try:
            self._train(**kwargs)
        except Exception as e:
            self._is_training = False
            raise e
        self._is_training = False
    def test(self, **kwargs):
        self._is_testing = True
        try:
            self._test(**kwargs)
        except Exception as e:
            self._is_testing = False
            raise e
        self._is_testing = False
    def validate(self, **kwargs):
        self._is_validating = True
        try:
            val_results = self._validate(**kwargs)
        except Exception as e:
            self._is_validating = False
            raise e
        self._is_validating = False
        return val_results
    def inference(self, **kwargs):
        pass
    

class SimpleClassifierMLModel(SimulationMLModel, InferenceModel):
    def __init__(self, model: Module) -> None:
        super().__init__(model)

    def produce(self, inputs: Union[torch.Tensor, torch.utils.data.Dataset]) -> torch.Tensor:
        device = get_available_accelerator()
        # Setup
        model               = self.model
        # Train
        model.eval()
        model.to(device)
        if isinstance(inputs, torch.Tensor):
            with torch.no_grad():
                inputs = inputs.to(device)
                pred = model(inputs)
                predictions = pred.argmax(1)
                return predictions
        elif isinstance(inputs, torch.utils.data.Dataset):
            tensors = []
            dl = DataLoader(inputs, batch_size=1, shuffle=False)
            with torch.no_grad():
                for (x,y) in dl:
                    x = x.to(device)
                    pred = model(x)
                    predictions = pred.argmax(1)
                    tensors.append(predictions)
            return torch.cat(tensors)

    def _train(self,
        dataloader: DataLoader,
        epochs:     int                             = 1,
        tb_logger:  Union[SummaryWriter, str, None] = None,
        log_step:   int                             = -1,
        loss_fn:    _Loss                           = None,
        optimizer:  Optimizer                       = None,
        do_val:     bool                            = False,
        val_per_steps:  int                         = -1,
        val_per_epoch:  int                         = -1,
        val_kwargs:     Dict[str, Any]              = {},
        step_callback: BaseCustomCallback           = EmptyCallback(),
        epoch_callback: BaseCustomCallback          = EmptyCallback(),
        device                                      = None,
        **kwargs
    ):
        step_callback.on_process_start(locals(), globals())
        epoch_callback.on_process_start(locals(), globals())
        step_callback.push_state("train")
        epoch_callback.push_state("train")
        # Get device
        if device is None:
            device = get_available_accelerator()
        # Setup tensorboard logger
        if isinstance(tb_logger, str):
            tb_logger = SummaryWriter(tb_logger)
        # Setup
        model               = self.model
        train_dataloader    = dataloader
        size                = len(train_dataloader.dataset)
        total_steps         = epochs * len(train_dataloader)
        loss_fn             = loss_fn \
            if loss_fn is not None \
            else nn.CrossEntropyLoss()
        optimizer           = optimizer \
            if optimizer is not None \
            else torch.optim.SGD(model.parameters(), lr=1e-3)

        # Train
        model.to(device)
        model.train()
        curr_steps = 0
        curr_samples = 0
        for epoch in range(1, epochs+1):
            for batch, (x, y) in enumerate(train_dataloader):
                x, y = x.to(device), y.to(device)

                pred = model(x)
                loss = loss_fn(pred, y)

                loss.backward()
                optimizer.step()
                optimizer.zero_grad()

                curr_steps += 1
                curr_samples += len(x)
                
                # Log loss
                if log_step > 0 and batch%log_step == 0:
                    train_loss = loss.item()
                    if tb_logger is not None:
                        tb_logger.add_scalar("loss/train", train_loss, curr_samples)
                # Validate every val_per_steps steps
                if do_val and val_per_steps > 0 and (curr_steps % val_per_steps  == 0):
                    val_results = self.validate(
                        device=device,
                        loss_fn=loss_fn,
                        **val_kwargs
                    )
                    model.train()
                    if tb_logger is not None and val_results is not None:
                        val_loss = val_results["loss"]
                        accuracy = val_results["correct_samples"] \
                            / val_results["total_samples"]
                        tb_logger.add_scalar("loss/val", val_loss, curr_samples)
                        tb_logger.add_scalar("acc/val", accuracy, curr_samples)
                # Perform callback
                step_callback.update_locals(locals())
                if not step_callback.on_invoke():
                    raise StopSimException(f"Invocation of step_callback at state '{step_callback.state}' terminated training.")
            # Validate every val_per_epoch epochs
            if do_val and val_per_epoch > 0 and (epoch % val_per_epoch == 0):
                val_results = self.validate(
                    device=device,
                    loss_fn=loss_fn,
                    **val_kwargs
                )
                model.train()
                if tb_logger is not None and val_results is not None:
                    val_loss = val_results["loss"]
                    accuracy = val_results["correct_samples"] \
                        / val_results["total_samples"]
                    tb_logger.add_scalar("loss/val", val_loss, curr_samples)
                    tb_logger.add_scalar("acc/val", accuracy, curr_samples)
            # Perform callback
            epoch_callback.update_locals(locals())
            if not epoch_callback.on_invoke():
                raise StopSimException(f"Invocation of epoch_callback at state '{epoch_callback.state}' terminated training.")
        # Pop callback states
        step_callback.pop_state()
        epoch_callback.pop_state()
        

    def _validate(
        self,
        dataloader: DataLoader,
        loss_fn:    _Loss                           = None,
        device                                      = None,
        **kwargs
    ):
        print(f"THIS IS VAL DATALOADER: {dataloader}")
        print(f"THIS IS VAL KWARGS: {kwargs}")
        if dataloader is None:
            return None
        print(f"VAL HERE")
        # Get device
        if device is None:
            device = get_available_accelerator()
        # Setup
        model               = self.model
        val_dataloader      = dataloader
        num_batches         = len(val_dataloader)
        num_samples         = len(val_dataloader.dataset)
        loss_fn             = loss_fn \
            if loss_fn is not None \
            else nn.CrossEntropyLoss()

        # Train
        model.to(device)
        model.eval()
        correct = 0
        test_loss = 0
        with torch.no_grad():
            for batch, (x, y) in enumerate(val_dataloader):
                x, y = x.to(device), y.to(device)

                pred = model(x)
                loss = loss_fn(pred, y)
                # Sum up total loss over validation
                test_loss += loss.item()
                # Sum up total correct samples. We divide by total samples later
                correct += (pred.argmax(1) == y).type(torch.float).sum().item()
        test_loss /= num_batches
        print(f"VAL DONE: {correct}")
        return {
            "loss": test_loss,
            "correct_samples": correct,
            "total_samples": num_samples
        }
