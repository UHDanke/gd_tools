# Imports
from typing import Self
from collections.abc import Iterator
import inspect


def filter_kwargs(func, kwargs):
    sig = inspect.signature(func)
    valid_params = sig.parameters
    return {k: v for k, v in kwargs.items() if k in valid_params}


class ListClass(list):
    
    def __init__(self, *args):
        super().__init__(*args)

    def __add__(self, other) -> Self:
        return self.__class__(super().__add__(other))


    def __radd__(self, other) -> Self:
        return self.__class__(other + list(self))


    def __mul__(self, n) -> Self:
        return self.__class__(super().__mul__(n))


    def __rmul__(self, n) -> Self:
        return self.__class__(super().__rmul__(n))


    def __getitem__(self, item) -> Self:
        result = super().__getitem__(item)
        return self.__class__(result) if isinstance(item, slice) else result


    def copy(self) -> Self:
        return self.__class__(self)
    
    
    def where(self, *conditions:callable, **kwargs) -> Self:
        """
        Filters a list where an item matches at least one condition.

        Parameters
        ----------
        *conditions : callable
            One or more functions that take in an object and return TRUE or FALSE.
            
        **kwargs : any
            Optional keyword arguments to pass to the called functions.

        Returns
        -------
        self
            A new class instance containing filtered objects.
            
        Example
        -------
        new_list = ListClass(1,2,3,4)
        
        filtered_list = new_list.where(lambda x: x>2)
        
        print(filtered_list)  # Output: [3, 4]
        """
        result = self.__class__()
        
        new_kwargs = list()
        
        for function in conditions:
            new_kwargs.append(filter_kwargs(function,kwargs))
        

        for item in self:
            for condition, nkwargs in zip(conditions, new_kwargs):
                if condition(item, **nkwargs):
                    result.append(item)
        
        return result
    
    
    def apply(self, *functions:callable, **kwargs) -> Self:
        """
        Applies a series of functions in place on each list member.

        Parameters
        ----------
        *functions : callable
            One or more functions that will be applied on each list member sequentially.

        **kwargs : any
            Optional keyword arguments to pass to the called functions.
            
        Returns
        -------
        self
            The class instance, allows method chaining.
            
        Example
        -------
        new_list = ListClass(1,2,3)
        
        new_list.apply(lambda x: x*2)
        
        print(new_list)  # Output: [2, 4, 6]

        """
        new_kwargs = list()
        
        for function in functions:
            new_kwargs.append(filter_kwargs(function,kwargs))
            
        for i, item in enumerate(self):
            for function, nkwargs in zip(functions,new_kwargs):
                if (val:=function(item, **nkwargs)) is not None:
                    self[i] = val
        
        return self
    
    
    def exclude(self, *conditions:callable, **kwargs) -> Self:
        """
        Returns all items that meet at least one condition and removes them from the list.

        Parameters
        ----------
        *conditions : callable
            One or more conditions that take in an object and return either TRUE or FALSE.

        **kwargs : any
            Optional keyword arguments to pass to the called functions.
            
        Returns
        -------
        self
            A new class instance containing the filtered objects.
         
        Example
        -------
            new_list = ListClass(1,2,3,4)
            
            filtered_list = new_list.where(lambda x: x>2)
            
            print(new_list) # Output: [1,2]
            
            print(filtered_list)  # Output: [3, 4]
        """
        ex = self.__class__()
        keep = []

        new_kwargs = list()
        
        for function in conditions:
            new_kwargs.append(filter_kwargs(function,kwargs))
              
        
        for item in self:
            for condition, nkwargs in zip(conditions, new_kwargs):
                if condition(item,**nkwargs):
                    ex.append(item)
                    break
            else:
                keep.append(item)
    
        self[:] = keep
        return ex
    
    
    def unique_values(self, *functions, **kwargs) -> set:
        """
        

        Parameters
        ----------
        *functions : TYPE
            DESCRIPTION.
        **kwargs : TYPE
            DESCRIPTION.

        Returns
        -------
        set
            DESCRIPTION.

        """
        result = set()
    
        if not functions:
            for item in self:
                result.update(item.values() or [])
                
        else:
            new_kwargs = list()
            
            for function in functions:
                new_kwargs.append(filter_kwargs(function,kwargs))
            
            for item in self:
                for function, nkwargs in zip(functions,new_kwargs):
                    result.update(function(item,**nkwargs) or [])
                
        return result
    
    
    def replace(self, value_map:dict) -> Self:
        
        for i, item in enumerate(self):
            self[i] = value_map.get(item, item)
            
        return self


class DictClass(dict):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
    @classmethod
    def fromkeys(cls, iterable, value=None):
        return cls({k: value for k in iterable})


    def __repr__(self):
        return f"{self.__class__}({dict(self)})"


    def copy(self):
        return self.__class__(self)


    def __or__(self, other):
        if not isinstance(other, dict):
            return NotImplemented
        return self.__class__(dict(self, **other))


    def __ror__(self, other):
        if not isinstance(other, dict):
            return NotImplemented
        return self.__class__(dict(other, **self))
    
    
    def pluck(self, *keys:str) -> list:
        """
        Retrieves the values of the specified keys from the object.

        Parameters
        ----------
        *keys : str
            One or more keys to retrieve the values of.

        Returns
        -------
        list
            Returns a list containing the values of the specified keys.

        """
        result = list()
        
        for k in keys:
            if (value := self.get(k)) is not None:
                result.append(value)
        
        return result


    def replace(self, *keys:str, value_map:dict=None, key_map:dict=None) -> Self:
        
        if not key_map or not value_map:
            return self
        
        value_map = value_map or {}
        key_map = key_map or {}
        
        new = {}
        
        for k in (keys or self.keys()):
            if (value := self.get(k)) is not None:
                new_key = key_map.get(k)
                new_value = value_map.get(value, self[k])
                
                if new_key is not None:
                    self.pop(k)
                    new[new_key] = new_value
                else:
                    new[k] = new_value
                
        self.update(new)
        
        return self
    
    
class DictList(ListClass):
    
    def __init__(self, *args):
        super().__init__(*args)
        
    
    def keys(self) -> Iterator[list]:
        
        for item in self:
            yield item.keys()
    
    
    def values(self) -> Iterator[list]:
        """
        

        Yields
        ------
        Iterator[list]
            DESCRIPTION.

        """
        for item in self:
            yield list(item.values())
    
    
    def items(self) -> Iterator[list]:
        
        for item in self:
            yield item.items()
            
    
    def keys_all(self) -> set:
        
        return set().union(*self.keys())
    
    
    def keys_common(self) -> set:
        
        try:
            return set.intersection(*self.keys())    
        except TypeError:
            return set()
    
    
class StrClass(str):
    
    def __new__(cls, value):
        return super().__new__(cls, value)
   
    
    def _wrap(self, result):
        return self.__class__(result) if isinstance(result, str) else result

    def __add__(self, other):
        return self._wrap(super().__add__(other))


    def __radd__(self, other):
        return self._wrap(other + super())


    def __getitem__(self, key):
        result = super().__getitem__(key)
        return self._wrap(result)


    def replace(self, old, new, count=-1):
        return self._wrap(super().replace(old, new, count))


    def upper(self):
        return self._wrap(super().upper())


    def lower(self):
        return self._wrap(super().lower())


    def capitalize(self):
        return self._wrap(super().capitalize())


    def title(self):
        return self._wrap(super().title())


    def strip(self, chars=None):
        return self._wrap(super().strip(chars))


    def lstrip(self, chars=None):
        return self._wrap(super().lstrip(chars))


    def rstrip(self, chars=None):
        return self._wrap(super().rstrip(chars))


    def join(self, iterable):
        return self._wrap(super().join(iterable))