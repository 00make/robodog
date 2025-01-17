from typing import Dict, Union, List
from .config import DEFAULT_PARAMS, UserMode

class DogController:
    """Dog Controller Class"""
    
    def __init__(self, client):
        self.client = client

    def set_user_mode(self, mode: Union[UserMode, int]) -> bool:
        """
        Set user mode
        
        Args:
            mode: User mode (can use UserMode enum)
            
        Returns:
            bool: Whether the setting was successful
        """
        if isinstance(mode, UserMode):
            mode = mode.value
            
        if not (1 <= mode <= 7):
            raise ValueError("Invalid user mode")

        try:
            self.client.publish(
                '/alphadog_node/set_user_mode',
                'ros_alphadog/SetUserMode',
                {'user_mode': mode}
            )
            return True
        except Exception as e:
            return False

    def set_parameters(self, params: Dict[str, float]) -> bool:
        """
        Set motion parameters
        
        Args:
            params: Parameter dictionary, see DEFAULT_PARAMS for available parameters
            
        Returns:
            bool: Whether the setting was successful
        """
        # Validate parameters
        for key in params:
            if key not in DEFAULT_PARAMS:
                raise ValueError(f"Unknown parameter: {key}")
        
        # Merge with default parameters
        full_params = DEFAULT_PARAMS.copy()
        full_params.update(params)
        
        request = self._build_parameter_request(full_params)
        try:
            result = self.client.call_service(
                '/alphadog_node/set_parameters',
                'dynamic_reconfigure/Reconfigure',
                request
            )
            return 'status' in result and result['status']
        except Exception as e:
            return False

    def _build_parameter_request(self, params: Dict[str, float]) -> Dict:
        """Build parameter request"""
        doubles = []
        ints = []
        
        # Distinguish between integer and float parameters
        for k, v in params.items():
            if isinstance(v, int):
                ints.append({'name': k, 'value': v})
            else:
                doubles.append({'name': k, 'value': float(v)})
                
        return {
            'config': {
                'doubles': doubles,
                'ints': ints,
                'bools': [],
                'strs': [],
                'groups': [
                    {'name': 'Default', 'state': True, 'id': 0, 'parent': 0},
                    {'name': 'remote_controller_config', 'state': True, 'id': 1, 'parent': 0}
                ]
            }
        }

    # def stand(self) -> bool:
    #     """Make the robot dog stand"""
    #     return self.set_user_mode(UserMode.STAND)

    # def walk(self) -> bool:
    #     """Enter walking mode"""
    #     return self.set_user_mode(UserMode.WALK)