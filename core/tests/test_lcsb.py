import pytest

from typing import Dict, List

from core.models import User
from core.lcsb.oidc import KeycloakAccountSynchronizer, KeycloakSynchronizationMethod
from core.lcsb.rems import create_rems_entitlement
from core.models.access import Access
from core.models.contact import Contact
from test.factories import ContactFactory, DatasetFactory, UserFactory
from web.views.utils import get_user_or_contact_by_oidc_id


class KeycloakAdminConnectionMock:
    def well_know(self) -> bool:
        return True

    def get_users(self, query) -> List[Dict]:
        return [{
            "id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", 
            "createdTimestamp": 1634231689999, 
            "username": "0000-0001-2222-3333", 
            "enabled": True, 
            "totp": False, 
            "emailVerified": True, 
            "firstName": "TESTY", 
            "lastName": "MCTesty", 
            "email": "testy.mctesty@uni.lu",
            "disableableCredentialTypes": [], 
            "requiredActions": [], 
            "notBefore": 0,
            "access": {
                "manageGroupMembership": False, 
                "view": True, 
                "mapRoles": False,
                "impersonate": False, 
                "manage": False
            }
        }, {
            "id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeef", 
            "createdTimestamp": 1634231689998, 
            "username": "0000-0001-2222-3334", 
            "enabled": True, 
            "totp": False, 
            "emailVerified": True, 
            "firstName": "BOBBY", 
            "lastName": "FISCHER", 
            "email": "bobby.fischer@gmail.com",
            "disableableCredentialTypes": [], 
            "requiredActions": [], 
            "notBefore": 0,
            "access": {
                "manageGroupMembership": False, 
                "view": True, 
                "mapRoles": False,
                "impersonate": False, 
                "manage": False
            }
        }, {
            "id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeeg", 
            "createdTimestamp": 1634231689997, 
            "username": "0000-0001-2222-3335", 
            "firstName": "Ann", 
            "lastName": "Bann", 
        }]
    

class KeycloakSynchronizationMethodMock(KeycloakSynchronizationMethod):
    def test_connection(self) -> bool:
        return True

    def __init__(self, config: Dict, connect=True) -> None:
        self.config = config
        self.keycloak_admin_connection = KeycloakAdminConnectionMock()

    @staticmethod
    def _validate_config(config: Dict) -> None:
        pass

    def get_keycloak_admin_connection(self) -> None:
        return KeycloakAdminConnectionMock()

    def _create_connection(self, config:Dict=None) -> KeycloakAdminConnectionMock:
        return KeycloakAdminConnectionMock()


def test_keycloak_synchronization_config_validation():
    with pytest.raises(KeyError):
        kc = KeycloakSynchronizationMethod({})
    
    with pytest.raises(KeyError):
        kc = KeycloakSynchronizationMethod({}, False)
        kc._create_connection({})


def test_keycloak_synchronization():
    mock = KeycloakSynchronizationMethodMock({}, False)
    synchronizer = KeycloakAccountSynchronizer(mock)

    current_external_accounts = mock.get_list_of_users()
    synchronizer.current_external_accounts = current_external_accounts
    accounts_to_be_created, accounts_to_be_patched, contacts_to_be_patched = synchronizer.compare()

    assert len(accounts_to_be_created) == 2, "There should be 2 new accounts to be added" 
    assert len(accounts_to_be_patched) == 0, "There should be no accounts to be patched"
    assert len(contacts_to_be_patched) == 0, "There should be no contacts to be patched"
    
    contact_count = Contact.objects.count()
    synchronizer._add_contacts(accounts_to_be_created)
    synchronizer._patch_users(accounts_to_be_patched)
    new_contact_count = Contact.objects.count()

    assert contact_count + 2 == new_contact_count

def test_add_rems_entitlements():
    elu_accession='12345678'

    user = UserFactory(oidc_id='12345', email='example@example.org')
    user.save()

    dataset = DatasetFactory(title='Test', local_custodians=[user], elu_accession=elu_accession)
    dataset.save()

    create_rems_entitlement(user, 'Test Application', elu_accession, user.oidc_id, user.email)
    user.delete()

def test_permissions():
    user = UserFactory(oidc_id='12345')
    user.save()

    user2 = UserFactory(oidc_id='23456')
    user2.save()

    contact = ContactFactory()
    contact.save()

    dataset = DatasetFactory(title='Test', local_custodians=[user], elu_accession='123', is_published=True)
    dataset.save()

    access = Access(access_notes='Access contact', contact=contact, dataset=dataset)
    access.save()

    access2 = Access(access_notes='Access user', user=user, dataset=dataset)
    access2.save()
    
    assert '123' in user.get_access_permissions()
    assert '123' in contact.get_access_permissions()
    assert len(user2.get_access_permissions()) == 0

def test_get_user_or_contact_by_oidc_id():
    user_found, contact_found, user, contact = get_user_or_contact_by_oidc_id('0')
    assert not user_found
    assert not contact_found

    user = UserFactory(oidc_id='123456')
    user.save()

    user_found, contact_found, user, contact = get_user_or_contact_by_oidc_id('123456')
    assert user_found
    assert not contact_found

    contact = ContactFactory(oidc_id='98765')
    contact.save()

    user_found, contact_found, user, contact = get_user_or_contact_by_oidc_id('98765')
    assert not user_found
    assert contact_found