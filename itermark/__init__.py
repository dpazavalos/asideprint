"""
Extensions of iterable data types, enabling bounds wise bookmarking indexing and active item setting
Enables iterable passing while preserving bookmarks
"""
from typing import Optional


class Itermark(list):
    """
    Extension of default list obj. Stores and preserves a bound wise bookmarking index that will
    never go outside of the underlying list's boundaries. Whole list can be passed between objects
    with bookmark

    - mark: Bookmark index of underlying list. Supports direct and operator assignment
    - active - list item, based off current mark index. Allows read/write usage
    """

    def __init__(self, iterable=None, ):
        """
        Extension of default list obj. Stores and preserves a bound wise bookmarking index that will
        never go outside of the underlying list's bounds. Whole list can be passed between objects
        with bookmark.

        Args:
            iterable:
                Iterable sequence to use. Mark
        """
        if isinstance(iterable, set):
            pass
            # todo extended type acceptance
            # tuple().__init__()
        elif isinstance(iterable, list):
            super().__init__(iterable)
        elif isinstance(iterable, str):
            super().__init__([iterable])
        elif not iterable:
            super().__init__([])
        else:
            raise TypeError("Currently unsupported type")

        self._mark = None
        """Protected bookmark index"""

    @property
    def mark(self) -> Optional[int]:
        """
        Get current active bookmark index

        Returns:
                Active bookmark index, or None if len=0
        """
        if self._is_loaded():
            return self._mark
        return None

    @mark.setter
    def mark(self, new_mark: int):
        """
        Attempts to set active mark, within bounds. OoBs marks are overwritten with closest bound

        Arguments:
            new_mark:
                Desired new bookmark index
        """
        if self._is_loaded():
            if not isinstance(new_mark, int):
                raise TypeError(f"marklist index must be integer, not {str(type(new_mark))}")

            # No negatives ( -= 1 fouls up indexing when _mark is 0)
            if new_mark < 0:
                self._mark = 0

            # Max length check
            elif self._mark >= self.__len__():
                self._mark = self.__len__() - 1

            else:
                self._mark = new_mark

    @property
    def active(self) -> any:
        """
        Get current active item, based off bookmark index

        Returns:
                Active item, or None if len=0
        """
        if self._is_loaded():
            return self[self._mark]
        return None

    @active.setter
    def active(self, val: any):
        """
        Set active list item, based on current mark value

        Args:
            val: new value for current actively marked list item
        """
        if self._is_loaded():
            self[self._mark] = val

    def _is_loaded(self) -> bool:
        """Used to prevent marklist functions if list is empty. All property functions call this"""
        if self.__len__() == 0:
            self._deactivate_mark()
            return False
        self._activate_mark()
        return True

    def _deactivate_mark(self):
        """Used to disable callable attributes, if list becomes []"""
        self._mark = None

    def _activate_mark(self):
        """Ensures _ndx is activated and within bounds. List is assumed active"""
        if not self._mark or self._mark < 0:
            self._mark = 0
        if self._mark >= self.__len__():
            self._mark = self.__len__() - 1
