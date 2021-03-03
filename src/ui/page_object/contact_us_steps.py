from src.ui.page_object.pages.contact_us_page import ContactUsPage


class ContactUsSteps(ContactUsPage):

    def contact_us_form_fill_all_fields(self):
        self.subject_heading_list_button_click()
