""" test ae.kivy_auto_width portion.

help/hints on how to make unit tests for kivy widgets running on gitlab-CI would be highly appreciated.
"""
from conftest import skip_gitlab_ci

from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget


from ae.kivy_auto_width import AutoFontSizeBehavior, ContainerChildrenAutoWidthBehavior, SimpleAutoTickerBehavior


def test_declaration():
    assert AutoFontSizeBehavior
    assert ContainerChildrenAutoWidthBehavior
    assert SimpleAutoTickerBehavior


class AutoFontLabel(AutoFontSizeBehavior, Label):
    """ test label """


@skip_gitlab_ci
class TestAutoFontSizeBehavior:
    def test_init(self):
        assert isinstance(AutoFontLabel(), AutoFontSizeBehavior)
        assert isinstance(AutoFontLabel(), Label)

    def test_resize(self):
        lbl = AutoFontLabel()
        fs = lbl.font_size
        lbl.text = "short txt"
        assert fs == lbl.font_size

    def test__font_size_adjustable(self):
        lbl = AutoFontLabel()
        assert lbl._font_size_adjustable() == 1
        lbl.text = "ver ver very very ver rry yyy loo ooo ooo ooo ooo ooo ooo ooo ooo ooo ooo ooo ooo ooo ooo ong text"
        lbl.texture_update()
        assert lbl._font_size_adjustable() == 0
        lbl.font_size = lbl.auto_font_max_size + 1
        assert lbl._font_size_adjustable() == -1

    def test__start_font_anim(self):
        lbl = AutoFontLabel()
        assert not lbl.texture_size[0]
        lbl._start_font_anim()

        lbl.text = "txt"
        lbl.texture_update()
        assert lbl._font_anim_mode == 1
        lbl.auto_font_max_size = lbl.font_size
        lbl._start_font_anim()

        lbl.auto_font_max_size = 66
        lbl._font_anim_mode = 1
        lbl._start_font_anim()
        assert lbl._font_size_anim

        lbl._stop_font_anim()
        lbl._ticker_text_updating = True
        lbl._start_font_anim()
        assert not lbl._font_size_anim

    def test__stop_font_anim(self):
        lbl = AutoFontLabel()
        lbl.text = "tst"
        lbl.texture_update()
        lbl.auto_font_max_size = 66
        lbl._font_anim_mode = 1
        lbl._start_font_anim()
        lbl._stop_font_anim()
        assert not lbl._font_size_anim

    def test__font_size_progress(self):
        lbl = AutoFontLabel()
        lbl._font_anim_mode = -1
        lbl._last_font_size = 33
        lbl.auto_font_min_size = 66
        lbl._font_size_progress(Animation(), Widget(), 1.0)
        assert lbl.font_size == 33
        assert lbl._last_font_size == 66


class ContWithoutOpen(ContainerChildrenAutoWidthBehavior, BoxLayout):
    """ boxlayout test - has no open method """
    close_called: bool = False
    dispatch_called = False

    def close(self, *args, **kwargs):
        """ overwritten to check if called correctly """
        self.close_called = True
        super().close(*args, **kwargs)

    def dispatch(self, name, *_args):
        """ patched to test if called. """
        if name == 'on_complete_opened':
            self.dispatch_called = True


class ContWithOpen(ContainerChildrenAutoWidthBehavior, Popup):
    """ container with open method """
    close_called: bool = False
    open_called: bool = False

    def close(self, *args, **kwargs):
        """ overwritten to check if called correctly """
        self.close_called = True
        super().close(*args, **kwargs)

    def open(self, *args, **kwargs):
        """ overwritten to check if called correctly """
        self.open_called = True
        super().open(*args, **kwargs)


@skip_gitlab_ci
class TestContainer:
    def test_init_without(self):
        con = ContWithoutOpen()
        assert con

    def test_init_with(self):
        con = ContWithOpen()
        assert con

    def test_close(self):
        con = ContWithoutOpen()
        con.close()
        assert con.close_called

        con = ContWithOpen()
        con.close()
        assert con.close_called

    def test_close_remove_from_parent(self):
        parent = Widget()
        con = ContWithoutOpen()
        parent.add_widget(con)
        assert con.parent and con in parent.children
        con.close()
        assert con.close_called
        assert not con.parent and con not in parent.children

    def test_on_complete_opened(self):
        con = ContWithoutOpen()
        assert not con.dispatch_called
        con._on_complete_opened()
        assert con.dispatch_called

    def test_open_without_parent_open(self, capsys):
        con = ContWithoutOpen()
        wid = Widget()
        out, err = capsys.readouterr()
        assert not out

        con.open(wid, animation=False)
        # out, err = capsys.readouterr()
        # assert "_open_width_progress" in out

    def test_open_with_parent_open(self, capsys):
        con = ContWithOpen()
        wid = Widget()
        out, err = capsys.readouterr()
        assert not out

        con.open(wid)
        assert con.open_called

        # out, err = capsys.readouterr()
        # assert "_open_width_progress" in out

    def test_progress_direct(self, capsys):
        con = ContWithoutOpen()
        out, err = capsys.readouterr()
        assert not out

        con._open_width_progress(Animation(), Widget(), 0.6)
        con.width = con.auto_width_minimum + 1

        con.container = Widget()
        con.width *= 3
        con._width_anim = Animation()
        con._open_width_progress(Animation(), Widget(), 0.6)
        for _ in range(3):
            con.container.add_widget(Widget())

        print(con.width)
        for chi in con.container.children:
            print(chi.width, chi)
            assert chi.width > 0    # == 100
        con._open_width_progress(Animation(), Widget(), 0.6)

    def test_open_without_anim(self, capsys):
        con = ContWithoutOpen()
        wid = Widget()
        out, err = capsys.readouterr()
        assert not out

        assert con.open(wid, animation=False) is None

    def test_reset_detected_complete_width(self):
        con = ContWithoutOpen()
        con._complete_width = 333
        con.reset_width_detection()
        assert not con._complete_width

    def test_win_width_range(self):
        con = ContWithOpen()
        wid = Widget()
        con.open(wid, animation=False)

        con.width = 0
        con._on_win_width()
        assert con.width >= con.auto_width_minimum


class TickerTestLabel(SimpleAutoTickerBehavior, Label):
    """ test ticker label """


@skip_gitlab_ci
class TestSimpleAutoTickerBehavior:
    def test_init(self):
        lbl = TickerTestLabel()
        assert isinstance(lbl, Label)
        assert isinstance(lbl, SimpleAutoTickerBehavior)

    def test__start_length_anim(self):
        lbl = TickerTestLabel()
        lbl._ori_text = "txt"
        lbl._start_length_anim()
        assert lbl.text == "txt"
        assert lbl._ori_text == "txt"
        assert lbl._length_anim

    def test__start_offset_anim(self):
        lbl = TickerTestLabel()
        lbl._start_offset_anim()
        assert lbl._offset_anim

    def test__stop_length_anim(self):
        lbl = TickerTestLabel()
        lbl._start_length_anim()
        lbl._stop_length_anim()
        assert not lbl._length_anim

    def test__stop_offset_anim(self):
        lbl = TickerTestLabel()
        lbl._start_offset_anim()
        lbl._stop_offset_anim()
        assert not lbl._offset_anim

    def test__ticker_length_progress(self):
        lbl = TickerTestLabel()
        lbl.text = "369"
        lbl._ticker_length_progress(Animation(), Widget(), 1.0)
        assert lbl.text == "369"

        lbl.text = "txt"
        lbl._ticker_texture_width = 333
        lbl._start_length_anim()
        lbl._ticker_length_progress(Animation(), Widget(), 1.0)
        assert lbl._ticker_text_length == SimpleAutoTickerBehavior._min_text_len

        long_txt = "ver ver very very ver rry yyy loo ooo ooo ooo ooo ooo ooo ooo ooo ooo ooo ooo ooo ooo ooo ong text"
        lbl.text = long_txt
        lbl.texture_update()
        lbl._ticker_texture_width = 333
        lbl._start_length_anim()
        lbl._ticker_length_progress(Animation(), Widget(), 1.0)
        assert lbl._ticker_text_length > SimpleAutoTickerBehavior._min_text_len
        assert len(lbl.text) < len(long_txt)

    def test__ticker_length_progress_halign_center(self):
        lbl = TickerTestLabel(halign='center')
        lbl.text = "369"
        lbl._ticker_length_progress(Animation(), Widget(), 1.0)
        assert lbl.text == "369"

        lbl.text = "txt"
        lbl._ticker_texture_width = 333
        lbl._start_length_anim()
        lbl._ticker_length_progress(Animation(), Widget(), 1.0)
        assert lbl._ticker_text_length == SimpleAutoTickerBehavior._min_text_len

        long_txt = "ver ver very very ver rry yyy loo ooo ooo ooo ooo ooo ooo ooo ooo ooo ooo ooo ooo ooo ooo ong text"
        lbl.text = long_txt
        lbl.texture_update()
        lbl._ticker_texture_width = 333
        lbl._start_length_anim()
        lbl._ticker_length_progress(Animation(), Widget(), 1.0)
        assert lbl._ticker_text_length > SimpleAutoTickerBehavior._min_text_len
        assert len(lbl.text) < len(long_txt)

    def test__ticker_offset_progress(self):
        lbl = TickerTestLabel()
        lbl.text = "txt"
        lbl._start_offset_anim()
        lbl._ticker_offset_progress(Animation(), Widget(), 1.0)
        assert not lbl._offset_anim     # anim starting delayed, and not starting if lbl is not visible (under root win)
