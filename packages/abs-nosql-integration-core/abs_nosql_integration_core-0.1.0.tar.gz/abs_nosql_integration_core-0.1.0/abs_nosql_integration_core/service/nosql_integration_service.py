from typing import Dict, Optional, List
from abs_nosql_integration_core.schema import TokenData
from abs_nosql_integration_core.repository import IntegrationRepository
from abs_exception_core.exceptions import NotFoundError
from abs_nosql_integration_core.utils import Encryption
from abs_nosql_integration_core.schema import Integration
from abs_nosql_repository_core.service import BaseService
from abs_integration_core.service import AbstractIntegrationBaseService


class IntegrationBaseService(BaseService, AbstractIntegrationBaseService):
    """
    Base class for all NoSQL integration services.
    Implements the IntegrationBaseService interface with NoSQL storage.
    """
    def __init__(
        self, 
        provider_name: str, 
        integration_repository: IntegrationRepository,
        encryption: Encryption
    ):
        self.provider_name = provider_name
        self.encryption = encryption
        super().__init__(integration_repository)

    async def get_query_by_provider(self):
        return await super().get_by_attr(
            attr="provider_name",
            value=self.provider_name
        )

    async def get_integration(self) -> Optional[TokenData]:
        """
        Get integration data.
        
        Returns:
            TokenData if integration exists, None otherwise
        """
        try:
            integration = await self.get_query_by_provider()
            return integration
        except Exception:
            return None

    async def get_all_integrations(self) -> List[Integration]:
        """
        Get all integrations.
        
        Returns:
            List of TokenData objects
        """
        try:
            integrations = await super().get_all()
            return integrations
        except Exception:
            return []

    async def delete_integration(self) -> bool:
        """
        Delete an integration.
        
        Returns:
            True if deleted, False otherwise
        """
        try:
            integration = await self.get_query_by_provider()
            await super().delete(integration["id"])

            return True

        except NotFoundError:
            # If the integration doesn't exist, consider it "deleted"
            return True

        except Exception as e:
            print(f"Error deleting integration: {str(e)}")
            return False
