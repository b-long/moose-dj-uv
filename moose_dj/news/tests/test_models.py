# Create your tests here.
from django.test import TestCase

# from news.models import MyModelName
from moose_dj.news.models import MyModelName

def saved_to_db(m_object, m_type) -> bool:
    saved_to_db = False
    saved_to_db = (
        m_object.pk is not None and m_type.objects.filter(pk=m_object.pk).exists()
    )
    return saved_to_db

class TestModels(TestCase):
    def setUp(self) -> None:
        self.model_1 = MyModelName.objects.create(
            my_field_name="Test MyModelName 1",
        )

        self.model_2 = MyModelName(
            my_field_name="Test MyModelName 2",
        )

        print("setUp complete")

    def test_persistence_behavior(self):
        """
        According to the docs as well as these StackOverflow discussions, the
        'create()' function will persist to the database immediately, while
        calling the constructor requires the caller to invoke 'save()'.

        More info:
            https://stackoverflow.com/q/26672077
            https://stackoverflow.com/q/2037320
            https://stackoverflow.com/q/907695
        """

        model_1_saved_to_db = not self.model_1._state.adding
        model_2_saved_to_db = not self.model_2._state.adding

        # Note: model_1 was created with 'create()', while
        #       model_2 was created with 'MyModelName()'
        self.assertTrue(model_1_saved_to_db)
        self.assertFalse(model_2_saved_to_db)

        # Once we invoke 'save()' the model is stored in the DB
        self.model_2.save()
        model_2_saved_to_db = not self.model_2._state.adding
        self.assertTrue(model_2_saved_to_db)

        # Since '_state' is a "private" attribute, we can assume
        # it's not officially supported.  Sachin's approach found
        # below will ensure an object is saved in the DB:
        #   https://stackoverflow.com/a/57564001
        self.assertTrue(saved_to_db(self.model_1, MyModelName))
        self.assertTrue(saved_to_db(self.model_2, MyModelName))