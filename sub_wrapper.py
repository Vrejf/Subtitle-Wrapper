import srt
import streamlit as st
import os
import zipfile
from datetime import datetime
import glob
import tempfile


wrapped_folder = "wrapped"
zip_folder_name = "zips"
uploads_folder = "uploads"
zipfile_name = "wrapd"


def wrap_line(text: str, line_wrap_limit: int = 42) -> str:
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


def wrap_files(temp_dir: str, limit: int = 40):
    for filepath in glob.glob(
        os.path.join(temp_dir, uploads_folder, "*.srt"), recursive=True
    ):
        subtitles = []
        with open(filepath, "r") as read_file:
            srt_file = srt.parse(read_file.read())
            subtitles = list(srt_file)
            subtitles = list(srt.sort_and_reindex(subtitles))
            for line in subtitles:
                line.content = line.content.strip()
                if len(line.content) > limit:
                    line.content = wrap_line(line.content, limit)
            subtitles = srt.compose(subtitles)
            savefile(subtitles, temp_dir, filepath)


def savefile(subtitles, dir, filename):
    """saves srt files

    Args:
        subtitles (substitle): the srt file
        dir (str): the directory to save the file
        filename (str): the name of the srt file
    """
    filepath = os.path.join(dir, wrapped_folder, os.path.basename(filename))

    with open(filepath, "w", encoding="utf-8") as write_file:
        write_file.write(subtitles)


def zip_folder(folder_path, output_path, zip_file_name_time):
    """Zips all the content of the wrapped folder

    Args:
        folder_path (str): input folder path
        output_path (str): output path
        zip_file_name_time (str): complete name of zip file
    """
    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
    with zipfile.ZipFile(
        os.path.join(output_path, zip_folder_name, f"{zipfile_name}_{timestamp}.zip"),
        "w",
    ) as zip_file:
        # for root, dirs, files in os.walk(os.path.join(folder_path, wrapped_folder)):
        #     for file in files:
        #         zip_file.write(os.path.join("wrapd", file))
        folder_path = os.path.join(folder_path, wrapped_folder)
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            arcname = os.path.basename(file_path)
            zip_file.write(file_path, arcname)


def print_content(path, dir: bool = True):
    print(f"-----All contents of path, dir={dir}-----")
    for file_path in glob.glob(path + "/**/*", recursive=True):
        if os.path.isdir(file_path) and dir:
            print(f"dir:\t{file_path}")
        elif os.path.isfile(file_path):
            print(f"file:\t{file_path}")


def preview_subs(sub_preview_win, wraplimit_slider, uploaded_file):
    """generates content for preview window

    Args:
        sub_preview_win (streamlit obj): Streamlit code box
        wraplimit_slider (int): wrap slider int
        uploaded_files (files): uploaded files
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        for name in [uploads_folder, wrapped_folder, zip_folder_name]:
            os.makedirs(os.path.join(temp_dir, name))
        path = os.path.join(temp_dir, uploads_folder, uploaded_file.name)
        with open(path, "wb") as f:
            f.write(uploaded_file.read())
        wrap_files(temp_dir, wraplimit_slider)
        previewtext = ""
        print(f"preview temp file:\t{os.path.join(temp_dir, uploaded_file.name)}")
        with open(
            os.path.join(temp_dir, wrapped_folder, uploaded_file.name), "r"
        ) as read_file:
            for i, line in enumerate(read_file):
                if i < 50:
                    previewtext += line
                elif i == 50:
                    previewtext += "..."
            sub_preview_win.code(previewtext)


def main():
    st.set_page_config(
        page_title="Wrap lines in SRT files",
    )
    st.title("Wrap lines in SRT files")

    uploaded_files = st.file_uploader(
        "Choose SRT-files, one or multiple.", accept_multiple_files=True, type=["srt"]
    )

    if "uploaded" not in st.session_state:
        st.session_state.uploaded = False

    wraplimit_slider = st.slider("Character wrap limit", 10, 80, 42, help="Default: 42")

    with st.expander("Preview", expanded=False):
        sub_preview_win = st.code("", language="json")

    if uploaded_files:
        # run_button.button("Run", disabled=False)
        st.session_state.uploaded = True
        preview_subs(sub_preview_win, wraplimit_slider, uploaded_files[0])
    else:
        # run_button.button("Run", disabled=True)
        st.session_state.uploaded = False
        sub_preview_win.code("No files uploaded")
    try:
        if st.session_state.uploaded:
            # create temp folders:
            with tempfile.TemporaryDirectory() as temp_dir:
                # Make folders:
                for name in [uploads_folder, wrapped_folder, zip_folder_name]:
                    os.makedirs(os.path.join(temp_dir, name))

                # filename for zip file
                timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
                zip_file_name_time = f"{zipfile_name}_{timestamp}.zip"

                # Do the Thing
                with st.spinner():
                    for file in uploaded_files:
                        path = os.path.join(temp_dir, uploads_folder, file.name)
                        with open(path, "wb") as f:
                            f.write(file.read())
                    wrap_files(temp_dir, wraplimit_slider)
                    # print_content(temp_dir)
                    zip_folder(temp_dir, temp_dir, zip_file_name_time)

                # Print all content of temp:
                # print_content(temp_dir, False)

                # if there is a zip, make Download button:
                if glob.glob(os.path.join(temp_dir, zip_folder_name, "*.zip")):
                    print("zip file exists check!")
                    # sleep(0.5)

                    # Download:
                    with open(
                        os.path.join(temp_dir, zip_folder_name, zip_file_name_time),
                        "rb",
                    ) as f:
                        st.caption("Done!")
                        download_button = st.download_button(
                            "Download File", f, zip_file_name_time
                        )
                        print(f"zip file: {f.name}")
    except:
        st.error("Something went wrong!")


if __name__ == "__main__":
    main()
