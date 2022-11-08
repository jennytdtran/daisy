import pytest
from django.shortcuts import reverse

from core.constants import Permissions
from test.factories import VIPGroup, DataStewardGroup, LegalGroup, AuditorGroup, ContactFactory, UserFactory
from .utils import check_response_status


def check_contact_view_permissions(url, user, action, contact):
    if action == Permissions.DELETE:
        # Only data stewards can delete a Contact instance
        if user.is_part_of(DataStewardGroup()):
            assert user.has_permission_on_object(f'core.{action.value}_contact', contact)
        else:
            assert not user.has_permission_on_object(f'core.{action.value}_contact', contact)

        check_response_status(url, user, [f'core.{action.value}_contact'], obj=contact)

    elif action is None:
        # Anyone can view or create a new Contact (no associated permission)
        check_response_status(url, user, [])

    elif action == Permissions.EDIT:
        # Anyone can edit a Contact instance
        check_response_status(url, user, [], obj=contact)

    else:
        # If other Permissions are needed, add the expected behavior
        raise ValueError(f"Unexpected permission {action} asked to work on Cohort instance")


@pytest.mark.parametrize('group', [VIPGroup, DataStewardGroup, LegalGroup, AuditorGroup])
@pytest.mark.parametrize(
    'destination_tuple',
    [
        ('contacts', None),
        ('contact_edit', Permissions.EDIT),
        ('contact_add', None),
        ('contact_delete', Permissions.DELETE),
        # FIXME: Needs to be discussed
        # ('contacts_export', None)
    ]
)
def test_contacts_views_permissions(permissions, group, destination_tuple):
    """
    Tests whether users from different groups can access the urls associated with Contact instances
    """
    # For now, anyone can create or edit contacts, but only datastewards can delete
    # FIXME
    #   Discuss this!
    url_name, action = destination_tuple

    contact = None
    if url_name in ['contacts', 'contact_add', 'contacts_export']:
        url = reverse(url_name)
    else:
        contact = ContactFactory()
        contact.save()
        url = reverse(url_name, kwargs={'pk': contact.pk})

    assert url is not None
    user = UserFactory(groups=[group()])
    check_contact_view_permissions(url, user, action, contact)
