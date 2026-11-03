import pytest

from playwright.sync_api import expect


class TestIFrames:

    def test_iframe_editor_has_default_text(self, open_internet):
        page = open_internet("iframe")
        frame = page.frame_locator("#mce_0_ifr")
        expect(frame.locator("#tinymce")).to_contain_text("Your content goes here.")

    def test_nested_frames_in_internet(self, open_internet):
        page = open_internet("nested_frames")

        nested_frame_middle = page.frame_locator(
            "frame[name='frame-top']"
        ).frame_locator("frame[name='frame-middle']")
        expect(nested_frame_middle.locator("#content")).to_have_text("MIDDLE")

        frame_bottom = page.frame_locator("frame[name='frame-bottom']")
        expect(frame_bottom.locator("body")).to_have_text("BOTTOM")


class TestNewTab:

    def test_new_window_launch_on_click_here(self, open_internet):
        page = open_internet("windows")

        with page.context.expect_page() as new_page_info:
            page.get_by_role("link", name="Click Here").click()

        new_page = new_page_info.value
        new_page.wait_for_load_state()
        expect(new_page.get_by_role("heading")).to_have_text("New Window")

        expect(page.get_by_role("heading")).to_have_text("Opening a new window")


class TestDialogs:

    def test_accept_alert_dialog(self, open_internet):
        page = open_internet("javascript_alerts")

        page.once("dialog", lambda dialog: dialog.accept())
        page.get_by_role("button", name="Click for JS Alert").click()
        expect(page.locator("#result")).to_have_text(
            "You successfully clicked an alert"
        )

    def test_dismiss_confirm_dialog(self, open_internet):
        page = open_internet("javascript_alerts")
        page.once("dialog", lambda dialog: dialog.dismiss())
        page.get_by_role("button", name="Click for JS Confirm").click()
        expect(page.locator("#result")).to_have_text("You clicked: Cancel")

    def test_accept_prompt_dialog_with_text(self, open_internet):
        page = open_internet("javascript_alerts")

        page.once("dialog", lambda dialog: dialog.accept("Alice"))
        page.get_by_role("button", name="Click for JS Prompt").click()
        expect(page.locator("#result")).to_have_text("You entered: Alice")

    @pytest.mark.parametrize("dialog_type, button_name, expected_dialog_message", [
        pytest.param("alert", "Click for JS Alert", "I am a JS Alert", id="alert_dialog"),
        pytest.param("confirm", "Click for JS Confirm", "I am a JS Confirm", id="confirm_dialog"),
        pytest.param("prompt", "Click for JS Prompt", "I am a JS prompt", id="prompt_dialog")
    ])
    def test_dialog_shows_expected_message(self, open_internet, dialog_type, button_name, expected_dialog_message):
        page = open_internet("javascript_alerts")
        messages = []                              
        captured = []
        def handle_dialog(dialog):                
            messages.append(dialog.message)        
            captured.append((dialog.type, dialog.message))
            dialog.accept()                        

        page.once("dialog", handle_dialog)         
        page.get_by_role("button", name=button_name).click()

        assert messages == [expected_dialog_message]     
        assert captured == [(dialog_type, expected_dialog_message)]


class TestUpload:

    def test_temp_file_upload(self, open_internet, tmp_path):

        page = open_internet("upload")

        path = tmp_path / "kyc_document.txt"
        path.write_text("test upload")

        page.locator("#file-upload").set_input_files(path)
        page.locator("#file-submit").click()
        expect(page.locator("#uploaded-files")).to_have_text(path.name)


class TestDownload:

    def test_file_download(self, open_internet, tmp_path):
        page = open_internet("download")

        with page.expect_download() as download_info:
            page.locator(".example a").first.click()

        download = download_info.value

        saved = tmp_path / download.suggested_filename
        download.save_as(saved)
        assert saved.exists() and saved.stat().st_size > 0
