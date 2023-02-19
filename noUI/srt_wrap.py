import srt
import argparse
import os


in_file = "Arabic short story-Arab_to_eng.srt"
out_file = "subtitles_wrapped.srt"
limit = 37


def wrap_line(text: str, line_wrap_limit: int = 50) -> str:
    """Wraps a line of text without breaking any word in half
    Args:
        text (str): Line text to wrap
        line_wrap_limit (int): Number of maximum characters in a line before wrap. Defaults to 50.
    Returns:
        str: Text line wraped
    """
    wraped_lines = []
    for word in text.split():
        # Check if inserting a word in the last sentence goes beyond the wrap limit
        if (
            len(wraped_lines) != 0
            and len(wraped_lines[-1]) + len(word) < line_wrap_limit
        ):
            # If not, add it to it
            wraped_lines[-1] += f" {word}"
            continue
        # Insert a new sentence
        wraped_lines.append(f"{word}")
    # Join sentences with line break
    return "\n".join(wraped_lines)


def savefile(subtitles):
    with open(out_file, "w", encoding="utf-8") as write_file:
        write_file.write(subtitles)


def main():
    subtitles = []
    with open(in_file, "r") as read_file:
        print(f"Reading file: {in_file}")
        srt_file = srt.parse(read_file.read())
        subtitles = list(srt_file)
        subtitles = list(srt.sort_and_reindex(subtitles))
        for line in subtitles:
            line.content = line.content.strip()
            if len(line.content) > limit:
                line.content = wrap_line(line.content, limit)

        subtitles = srt.compose(subtitles)
        print(f"Saving file: {out_file}")
        savefile(subtitles)
        # with open(out_file, "w", encoding="utf-8") as write_file:
        #    write_file.write(subtitles)


if __name__ == "__main__":
    main()
