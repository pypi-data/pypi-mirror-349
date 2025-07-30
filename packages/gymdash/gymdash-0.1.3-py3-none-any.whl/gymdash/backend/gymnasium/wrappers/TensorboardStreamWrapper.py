import os
from typing import Any, Dict, Iterable, List, Set, SupportsFloat, Union

from gymdash.backend.core.api.config.config import CONFIG
from gymdash.backend.core.api.config.stat_tags import ANY_TAG

try:
    import gymnasium as gym
    _has_gym = True
except ImportError:
    _has_gym = False
    

try:
    from tensorboard.backend.event_processing import (event_accumulator,
                                                      tag_types)
    _has_tensorboard = True
except ImportError:
    _has_tensorboard = False
    

from gymdash.backend.tensorboard.TensorboardStreamableStat import \
    TensorboardStreamableStat

if not _has_gym:
    raise ImportError("Install gymnasium to use gymdash environment wrappers.")
if not _has_tensorboard:
    raise ImportError("Install tensorboard to use gymdash environment wrappers.")


class TensorboardStreamWrapper(gym.Wrapper):
    def __init__(self, env: gym.Env, tb_log: str, tag_key_map: Union[Dict[str,List[str]],None]=None):
        super().__init__(env)
        self.streamer = TensorboardStreamer(tb_log, tag_key_map)

    def reset(self, **kwargs) -> tuple[Any, dict[str, Any]]:
        return self.env.reset(**kwargs)
    
    def render(self):
        return self.env.render()
    
    def close(self):
        return self.env.close()
    
    def step(self, action: Any) -> tuple[Any, SupportsFloat, bool, bool, dict[str, Any]]:
        return self.env.step(action)
    


    def get_stat_keys(self):
        return self.streamer.get_stat_keys()
        
    @property
    def streamer_name(self):
        return self.streamer.streamer_name
        
    def add_tag_keys(self, tag_key_map:Dict[str, Iterable[str]]):
        self.streamer.add_tag_keys(tag_key_map)
    
    def set_log_path(self, new_path):
        self.streamer.set_log_path(new_path)

    def Reload(self):
        self.streamer.Reload()
    
    def get_all_from_tag(self, tag: str):
        return self.streamer.get_all_from_tag(tag)
    
    def get_all_recent(self):
        return self.streamer.get_all_recent()
    
    def get_recent_from_tag(self, tag: str):
        return self.streamer.get_recent_from_tag(tag)

    def get_recent_from_key(self, key:str) -> List[Any]:
        return self.streamer.get_recent_from_key(key)
    
    def reset_streamer(self):
        self.streamer.reset_streamer()
    
        

class TensorboardStreamer:
    def __init__(self, tb_log: str, tag_key_map: Union[Dict[str,List[str]],None]=None):
        self.tb_log_path: str                           = tb_log
        self._tb_exists: bool                           = False
        self._ea: event_accumulator.EventAccumulator    = None
        # self.keys: Set[str]                             = set(keys) if keys else set()
        if tag_key_map is None:
            self.keys = set()
        else:
            self.keys = set([x for xs in tag_key_map.values() for x in xs])

        self.tag_key_map: Dict[str, Set[str]] = {
            ANY_TAG: set(),
            tag_types.TENSORS:                  set(),
            tag_types.RUN_METADATA:             set(),
            tag_types.COMPRESSED_HISTOGRAMS:    set(),
            tag_types.HISTOGRAMS:               set(),
            tag_types.IMAGES:                   set(),
            tag_types.AUDIO:                    set(),
            tag_types.SCALARS:                  set(),
        }
        self.key_tag_map: Dict[str, Set[str]] = {
            # key: set((ANY_TAG,)) for key in self.keys
            key: set() for key in self.keys
        }
        self.add_tag_keys(tag_key_map)

        # Streamed maps key names to StreamableStats
        self.streamed: Dict[str, TensorboardStreamableStat] = {}
        # streamed_tag_exclusive is EXCLUSIVE in the sense that a streamable stat
        # is only under a SINGLE tag in streamed_tag_exclusive even if that stat
        # has multiple associated_tags.
        self.streamed_tag_exclusive: Dict[str, Set[TensorboardStreamableStat]] = {}

    def get_stat_keys(self):
        # TODO: Don't be stupid. Please don't be stupied
        # Every key should just have one, specific tag.
        # You are overcomplicating this.
        return [(key, list(self.key_tag_map[key])[0]) for key in self.keys]
        
    @property
    def streamer_name(self):
        return self.tb_log_path
    
    def reset_streamer(self):
        self.set_log_path(self.tb_log_path)
        self.check_tb()
        
    def add_tag_keys(self, tag_key_map:Dict[str, Iterable[str]]):
        # Combine the input tag key map
        if tag_key_map:
            for tag in tag_key_map.keys():
                keys = tag_key_map[tag]
                # Extend the current key set
                self.keys.update(keys)
                # Extend the tag -> keys map
                if tag in self.tag_key_map:
                    self.tag_key_map[tag].update(keys)
                else:
                    self.tag_key_map[tag] = set(keys)
            for tag in tag_key_map.keys():
                keys = tag_key_map[tag]
                print(f"TensorboardStreamer Adding keys: {keys}")
                # Extend the key -> tags map
                for key in keys:
                    if key in self.key_tag_map:
                        self.key_tag_map[key].add(tag)
                    else:
                        self.key_tag_map[key] = set(tag)
        print(f"TensorboardStreamer New tag_key_map: {self.tag_key_map}")
        print(f"TensorboardStreamer New key_tag_map: {self.key_tag_map}")
    
    def set_log_path(self, new_path):
        self.tb_log_path = new_path
        self._tb_exists = False
        self.streamed.clear()
        self.streamed_tag_exclusive.clear()

    # https://github.com/tensorflow/tensorboard/blob/master/tensorboard/backend/event_processing/event_accumulator.py#L940
    def check_tb(self):
        if (self._tb_exists): return True
        if (not self.tb_log_path): return False
        # Setup using new EventAccumulator
        self._ea = event_accumulator.EventAccumulator(
            os.path.abspath(self.tb_log_path),
            size_guidance=CONFIG.tb_size_guidance
        )
        # Check for existence of folder after EA, so that it
        # has a chance to build
        if (not os.path.exists(os.path.abspath(self.tb_log_path))): return False
        # Create new TensorboardStreamableStats for all keys under each tag
        for tag, keys in self.tag_key_map.items():
            self.streamed_tag_exclusive[tag] = set()
            for key in keys:
                streamed_stat = TensorboardStreamableStat(self._ea, key, self.key_tag_map[key])
                self.streamed[key] = streamed_stat
                self.streamed_tag_exclusive[tag].add(streamed_stat)

        self._tb_exists = True
        return True
    
    def Reload(self):
        if self.check_tb():
            self._ea.Reload()

    def _valid_stats(self, tag: str):
        """Returns stats whose determined tag is tag."""
        # [stat for stat in self.streamed.values() if stat.found_key_tag==tag]
        # return self.streamed_tag_exclusive[tag].union(self.streamed_tag_exclusive[ANY_TAG])
        return [stat for stat in self.streamed.values() if stat.found_key_tag==tag]
    
    def get_all_from_tag(self, tag: str):
        if self.check_tb():
            # self._ea.Reload()
            return {stat.key: stat.get_values() for stat in self._valid_stats(tag)}
        return {stat.key: [] for stat in self._valid_stats(tag)}
    
    def get_all_recent(self):
        if self.check_tb():
            # self._ea.Reload()
            return {key: self.streamed[key].get_recent() for key in self.keys}
        return {key: [] for key in self.keys}
    
    def get_recent_from_tag(self, tag: str):
        print(f"TensorboardStreamer get_recent_from_tag: '{tag}'")
        print(f"TensorboardStreamer valid stats: '{self._valid_stats(tag)}'")
        if self.check_tb():
            # self._ea.Reload()
            return {stat.key: stat.get_recent() for stat in self._valid_stats(tag)}
        return {key: [] for key in self.streamed_tag_exclusive[tag]}

    def get_recent_from_key(self, key:str) -> List[Any]:
        print(f"TensorboardStreamer get_recent_from_key: '{key}'")
        if self.check_tb():
            # self._ea.Reload()
            if key in self.streamed:
                return self.streamed[key].get_recent()
            else:
                return []
        return []