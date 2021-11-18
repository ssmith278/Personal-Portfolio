from unittest.case import SkipTest, skip
from django.test import TestCase, tag
from django.core.validators import ValidationError
from .models import ContactInfo, Education, Employment, Resume

# Create your tests here.
def test_validator_fail(testcase, obj, **kwargs):
    
    with testcase.assertRaises(ValidationError):
        if obj.full_clean():
            obj.save()
    
    testcase.assertEqual(obj.__class__.objects.filter(**kwargs).count(), 0)

class ContactInfoModelTests(TestCase):
    @tag('fast', 'validator', 'phone')
    def test_phone_num_short_length(self):

        contact_info = ContactInfo()
        contact_info.phone_number = '1'

        test_validator_fail(self, contact_info, phone_number='1')
    
    @tag('fast', 'validator', 'phone')
    def test_phone_num_long_length(self):

        contact_info = ContactInfo()
        contact_info.phone_number = '12345678901234567890'

        test_validator_fail(self, contact_info, phone_number='12345678901234567890')

    @tag('fast', 'validator', 'phone')
    def test_phone_num_normal_length(self):

        contact_info = ContactInfo()
        contact_info.phone_number = '1234567890'

        contact_info.save()

        self.assertEqual(ContactInfo.objects.filter(phone_number='1234567890').count(), 1)

class ResumeModelTest(TestCase):

    def test_singular_choice(self):

        resume = Resume(
            full_name = 'Resume1',
            is_chosen = True   
        )

        resume.save()

        self.assertEqual(Resume.objects.filter(is_chosen=True).count(), 1)
        self.assertEqual(Resume.objects.filter(is_chosen=True).first().full_name, resume.full_name)

        resume2 = Resume(
            full_name = 'Resume2',
            is_chosen = True
        )

        resume2.save()

        self.assertEqual(Resume.objects.filter(is_chosen=True).count(), 1)
        self.assertEqual(Resume.objects.filter(is_chosen=True).first().full_name, resume2.full_name)
