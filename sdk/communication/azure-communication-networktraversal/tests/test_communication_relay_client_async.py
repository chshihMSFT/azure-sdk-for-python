# coding: utf-8
# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
from azure.core.credentials import AccessToken
from azure.communication.identity.aio import CommunicationIdentityClient
from azure.communication.networktraversal import RouteType
from azure.communication.identity._api_versions import ApiVersion
from azure.communication.networktraversal.aio import CommunicationRelayClient
from _shared.helper import URIIdentityReplacer
from _shared.testcase import (
    BodyReplacerProcessor
)
from _shared.asynctestcase  import AsyncCommunicationTestCase
from _shared.communication_service_preparer import CommunicationPreparer
from _shared.utils import get_http_logging_policy
from _shared.utils import parse_connection_str
from azure.identity.aio import DefaultAzureCredential

class FakeTokenCredential(object):
    def __init__(self):
        self.token = AccessToken("Fake Token", 0)

    def get_token(self, *args):
        return self.token

class CommunicationRelayClientTestAsync(AsyncCommunicationTestCase):
    def setUp(self):
        super(CommunicationRelayClientTestAsync, self).setUp()
        self.recording_processors.extend([
            BodyReplacerProcessor(keys=["id", "token", "username", "credential"]),
            URIIdentityReplacer()])

    @CommunicationPreparer()
    async def test_get_relay_configuration(self, communication_livetest_dynamic_connection_string):
        identity_client = CommunicationIdentityClient.from_connection_string(
            communication_livetest_dynamic_connection_string,
            http_logging_policy=get_http_logging_policy()
        )

        async with identity_client: 
            user = await identity_client.create_user()        

        networkTraversalClient = CommunicationRelayClient.from_connection_string(
            communication_livetest_dynamic_connection_string,
            http_logging_policy=get_http_logging_policy()
        )

        async with networkTraversalClient:
            print('Getting relay config:\n')
            config = await networkTraversalClient.get_relay_configuration(user=user)
        
        for iceServer in config.ice_servers:
            assert iceServer.username is not None
            print('Username: ' + iceServer.username)

            assert iceServer.credential is not None
            print('Credential: ' + iceServer.credential)
            
            assert iceServer.urls is not None
            for url in iceServer.urls:
                print('Url:' + url)

            assert iceServer.route_type is not None

        assert config is not None
    
    @CommunicationPreparer()
    async def test_get_relay_configuration_without_identity(self, communication_livetest_dynamic_connection_string):     

        networkTraversalClient = CommunicationRelayClient.from_connection_string(
            communication_livetest_dynamic_connection_string,
            http_logging_policy=get_http_logging_policy()
        )

        async with networkTraversalClient:
            print('Getting relay config:\n')
            config = await networkTraversalClient.get_relay_configuration()
        
        print('Ice Servers Async:\n')
        for iceServer in config.ice_servers:
            assert iceServer.username is not None
            print('Username: ' + iceServer.username)

            assert iceServer.credential is not None
            print('Credential: ' + iceServer.credential)
            
            assert iceServer.urls is not None
            for url in iceServer.urls:
                print('Url:' + url)

        assert config is not None
        
    @CommunicationPreparer()
    async def test_get_relay_configuration_with_route_type_nearest(self, communication_livetest_dynamic_connection_string):
        identity_client = CommunicationIdentityClient.from_connection_string(
            communication_livetest_dynamic_connection_string,
            http_logging_policy=get_http_logging_policy()
        )

        async with identity_client: 
            user = await identity_client.create_user()        

        networkTraversalClient = CommunicationRelayClient.from_connection_string(
            communication_livetest_dynamic_connection_string,
            http_logging_policy=get_http_logging_policy()
        )

        async with networkTraversalClient:
            print('Getting relay config with nearest type:\n')
            config = await networkTraversalClient.get_relay_configuration(user=user, route_type=RouteType.NEAREST)
        
        print('Ice Servers Async:\n')
        for iceServer in config.ice_servers:
            assert iceServer.username is not None
            print('Username: ' + iceServer.username)

            assert iceServer.credential is not None
            print('Credential: ' + iceServer.credential)
            
            assert iceServer.urls is not None
            for url in iceServer.urls:
                print('Url:' + url)
            
            assert iceServer.route_type == RouteType.NEAREST

        assert config is not None

    @CommunicationPreparer()
    async def test_get_relay_configuration_with_route_type_any(self, communication_livetest_dynamic_connection_string):
        identity_client = CommunicationIdentityClient.from_connection_string(
            communication_livetest_dynamic_connection_string,
            http_logging_policy=get_http_logging_policy()
        )

        async with identity_client: 
            user = await identity_client.create_user()        

        networkTraversalClient = CommunicationRelayClient.from_connection_string(
            communication_livetest_dynamic_connection_string,
            http_logging_policy=get_http_logging_policy()
        )

        async with networkTraversalClient:
            print('Getting relay config with nearest type:\n')
            config = await networkTraversalClient.get_relay_configuration(user= user, route_type=RouteType.ANY)
        
        print('Ice Servers Async:\n')
        for iceServer in config.ice_servers:
            assert iceServer.username is not None
            print('Username: ' + iceServer.username)

            assert iceServer.credential is not None
            print('Credential: ' + iceServer.credential)
            
            assert iceServer.urls is not None
            for url in iceServer.urls:
                print('Url:' + url)
            
            assert iceServer.route_type == RouteType.ANY

        assert config is not None
        