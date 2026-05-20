from mindbuddy.tui.chrome import (
    get_permission_prompt_max_scroll_offset,
    render_banner,
    render_footer_bar,
    render_panel,
    render_permission_prompt,
    render_slash_menu,
    render_status_line,
    render_tool_panel,
)
from mindbuddy.tui.input import render_input_prompt
from mindbuddy.tui.input_parser import (
    KeyEvent,
    ParsedInputEvent,
    ParseResult,
    TextEvent,
    WheelEvent,
    parse_input_chunk,
)
from mindbuddy.tui.markdown import render_markdownish
from mindbuddy.tui.screen import (
    clear_screen,
    enter_alternate_screen,
    exit_alternate_screen,
    hide_cursor,
    show_cursor,
)
from mindbuddy.tui.theme import ColorTheme, theme
from mindbuddy.tui.transcript import (
    format_transcript_text,
    get_transcript_max_scroll_offset,
    get_transcript_window_size,
    render_transcript,
)
from mindbuddy.tui.types import TranscriptEntry

__all__ = [
    # screen
    "clear_screen",
    "enter_alternate_screen",
    "exit_alternate_screen",
    "hide_cursor",
    "show_cursor",
    # chrome
    "get_permission_prompt_max_scroll_offset",
    "render_banner",
    "render_footer_bar",
    "render_panel",
    "render_permission_prompt",
    "render_slash_menu",
    "render_status_line",
    "render_tool_panel",
    # input
    "render_input_prompt",
    # input_parser
    "KeyEvent",
    "ParsedInputEvent",
    "ParseResult",
    "TextEvent",
    "WheelEvent",
    "parse_input_chunk",
    # markdown
    "render_markdownish",
    # theme
    "ColorTheme",
    "theme",
    # transcript
    "format_transcript_text",
    "get_transcript_max_scroll_offset",
    "get_transcript_window_size",
    "render_transcript",
    # types
    "TranscriptEntry",
]
