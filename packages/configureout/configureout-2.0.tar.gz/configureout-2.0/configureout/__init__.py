import json
import uuid
from types import SimpleNamespace



class RootConfigTypeError(TypeError):
	def __init__(self, obj):
		super().__init__(f'Root config must be a dict or string, not {type(obj).__name__}')


class ConfigLoadedError(ValueError):
	def __init__(self):
		super().__init__('Config is already loaded')


class ConfigPathError(ValueError):
	def __init__(self):
		super().__init__('Attribute "config_path" is required for non-file configs')


class Config(SimpleNamespace):
	__slots__ = (f'meta_{uuid.uuid4().hex}',)

	def __init__(self, config=None, **io_params):
		self._meta = SimpleNamespace(
			loaded=False,
			type=None,
			io_params={
				'encoding': 'utf-8', **io_params
			}
		)

		if config:
			if type(config) == str:
				try:
					self.from_string(config)
				except:
					self.from_file(config)
	
			elif type(config) == dict:
				self.from_dict(config)
			else:
				raise RootConfigTypeError(config)

	@property
	def _meta(self):
		return getattr(self, self.__slots__[0])
	
	@_meta.setter
	def _meta(self, value):
		setattr(self, self.__slots__[0], value)

	def from_file(self, config_path, **kwargs):
		with open(config_path, 'r', **self._meta.io_params) as f:
			config = f.read()
			self.from_string(config, **kwargs)

		self._meta.type = 'file'

	def from_string(self, config_string, **kwargs):
		config = json.loads(config_string, **kwargs)
		self.from_dict(config)

		if not self._meta.type:
			self._meta.type = 'string'

	def from_dict(self, config_dict):
		if self._meta.loaded:
			raise ConfigLoadedError()
		
		ns = self._to_namespace(config_dict)
		super().__init__(**ns.__dict__)
		
		if not self._meta.type:
			self._meta.type = 'dict'
		self._meta.loaded = True

	def _to_namespace(self, obj):
		if isinstance(obj, dict):
			return SimpleNamespace(**{k: self._to_namespace(v) for k, v in obj.items()})
		elif isinstance(obj, list):
			return [self._to_namespace(i) for i in obj]
		else:
			return obj

	def keys(self): return self.__dict__.keys()

	def values(self): return self.__dict__.values()

	def items(self): return self.__dict__.items()

	def get(self, key, default=None): return self.__dict__.get(key, default)

	def to_dict(self):
		return self._to_dict(self)

	def _to_dict(self, obj):
		if isinstance(obj, SimpleNamespace):
			return {k: self._to_dict(v) for k, v in vars(obj).items()}
		elif isinstance(obj, list):
			return [self._to_dict(i) for i in obj]
		else:
			return obj
	
	def save(self, config_path=None, **kwargs):
		if not config_path:
			if self._meta.type == 'file':
				config_path = self._meta.config
			else:
				raise ConfigPathError()

		with open(config_path, 'w', **self._meta.io_params) as f:
			json.dump(self.to_dict(), f, **kwargs)
			
	def update(self, other=None, **kwargs):
		other = other or {}
		for k, v in dict(other, **kwargs).items():
			self[k] = v
	
	def copy(self):
		return Config(data=self.to_dict())
	
	def __getitem__(self, key): return self.__dict__[key]

	def __setitem__(self, key, value): self.__dict__[key] = value

	def __delattr__(self, key): del self.__dict__[key]

	def __contains__(self, key): return key in self.__dict__

	def __len__(self): return len(self.__dict__)

	def __iter__(self): return iter(self.__dict__)

	def __str__(self): return json.dumps(self.to_dict(), indent=4, ensure_ascii=False, default=str)

	def __repr__(self): return f"{self.__class__.__name__}({self.__dict__})"

	def __reduce__(self): return (self.__class__, (), self.__dict__)

	def __bool__(self): return bool(self.__dict__)

	def __eq__(self, other):
		if isinstance(other, Config):
			return self.to_dict() == other.to_dict()
		elif isinstance(other, dict):
			return self.to_dict() == other
		return False

	def __or__(self, other):
		result = Config(config=self.to_dict())
		result.update(other)
		return result
	
	def __ior__(self, other):
		self.update(other)
		return self
