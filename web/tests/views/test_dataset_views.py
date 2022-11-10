import pytest
from typing import Optional
from django.shortcuts import reverse
from django.test.client import Client

from test.factories import VIPGroup, DataStewardGroup, LegalGroup, AuditorGroup, DatasetFactory, UserFactory, DatasetDocumentFactory
from core.constants import Permissions
from core.models.user import User
from core.models.dataset import Dataset
from .utils import check_response_status


def check_dataset_views_permissions(url: str, user: User, action: Permissions, dataset: Optional[Dataset]):
    if action:
        if user.is_part_of(DataStewardGroup()):
            assert user.has_permission_on_object(f'core.{action.value}_dataset', dataset)
            check_response_status(url, user, [f'core.{action.value}_dataset'], dataset)
        else:
            assert not user.has_permission_on_object(f'core.{action.value}_dataset', dataset)
            check_response_status(url, user, [f'core.{action.value}_dataset'], dataset)

            dataset.local_custodians.set([user])
            assert user.has_permission_on_object(f'core.{action.value}_dataset', dataset)
            check_response_status(url, user, [f'core.{action.value}_dataset'], dataset)

    else:
        check_response_status(url, user, [], dataset)


@pytest.mark.parametrize('group', [VIPGroup, DataStewardGroup, LegalGroup, AuditorGroup])
@pytest.mark.parametrize(
    'url_name, action',
    [
        ('datasets', None),
        ('datasets_export', None),
        ('dataset_add', None),
        ('dataset', None),
        ('dataset_delete', Permissions.DELETE),
        ('dataset_edit', Permissions.EDIT),
        # FIXME: What permissions to use here?
        ('dataset_publish', None),
        ('dataset_unpublish', None)
    ]
)
def test_dataset_views_permissions(permissions, group, url_name, action):
    """
    Tests whether users from different groups can access urls associated with Dataset instances
    """
    dataset = None
    if url_name in ['datasets', 'datasets_export', 'dataset_add']:
        url = reverse(url_name)
    else:
        dataset = DatasetFactory()
        dataset.save()
        url = reverse(url_name, kwargs={"pk": dataset.pk})

    assert url is not None
    user = UserFactory(groups=[group()])
    check_dataset_views_permissions(url, user, action, dataset)

# FIXME
@pytest.mark.skip("Dataset templates do not display documents")
@pytest.mark.parametrize('group', [VIPGroup, DataStewardGroup, LegalGroup, AuditorGroup])
def test_dataset_view_protected_documents(permissions, group):
    dataset = DatasetFactory()
    user = UserFactory(groups=[group()])

    client = Client()
    client.login(username=user.username, password=user.password)

    url = reverse('dataset', kwargs={"pk": dataset.pk})
    response = client.get(url, follow=True)

    if user.is_part_of(DataStewardGroup()) or user.is_part_of(AuditorGroup()):
        assert b'<div class="row mt-4" id="documents-card">' in response.content
        assert b'<h2 class="card-title"><span><i class="material-icons">link</i></span> Documents</h2>' in response.content
    else:
        assert b'<div class="row mt-4" id="documents-card">' not in response.content
        assert b'<h2 class="card-title"><span><i class="material-icons">link</i></span> Documents</h2>' not in response.content

    if user.is_part_of(VIPGroup()):
        dataset.local_custodians.set([user])
        response = client.get(url, follow=True)
        assert b'<div class="row mt-4" id="documents-card">' in response.content
        assert b'<h2 class="card-title"><span><i class="material-icons">link</i></span> Documents</h2>' in response.content


@pytest.mark.skip("Dataset templates do not display documents")
@pytest.mark.parametrize('group', [VIPGroup, DataStewardGroup, LegalGroup, AuditorGroup])
def test_dataset_edit_protected_documents(permissions, group):
    document = DatasetDocumentFactory()
    dataset = document.content_object

    user = UserFactory(groups=[group()])

    client = Client()
    assert client.login(username=user.username, password='test-user'), "Login failed"

    url = reverse('dataset', kwargs={"pk": dataset.pk})
    response = client.get(url, follow=True)

    if user.is_part_of(DataStewardGroup()):
        assert b'<div class="ml-1 float-right btn-group" id="add-dataset-document">' in response.content
        assert b'<th id="document-action-head" style="width:7em">Actions</th>' in response.content
        assert b'<td id="document-action">' in response.content

    else:
        assert b'<div class="ml-1 float-right btn-group" id="add-dataset-document">' not in response.content
        assert b'<th id="document-action-head" style="width:7em">Actions</th>' not in response.content
        assert b'<td id="document-action">' not in response.content

    if user.is_part_of(VIPGroup()):
        dataset.local_custodians.set([user])
        response = client.get(url, follow=True)
        assert b'<div class="ml-1 float-right btn-group" id="add-dataset-document">' in response.content
        assert b'<th id="document-action-head" style="width:7em">Actions</th>' in response.content
        assert b'<td id="document-action">' in response.content

