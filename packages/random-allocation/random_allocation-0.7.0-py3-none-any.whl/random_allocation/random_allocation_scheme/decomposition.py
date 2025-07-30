# Standard library imports
from typing import Optional, Union, Callable, Dict, Any, List, Tuple, Literal

# Third-party imports
import numpy as np
from dp_accounting.pld.privacy_loss_distribution import PrivacyLossDistribution

# Local application imports
from random_allocation.comparisons.utils import search_function_with_bounds, FunctionType, BoundType
from random_allocation.other_schemes.poisson import Poisson_delta_PLD, Poisson_epsilon_PLD, Poisson_PLD
from random_allocation.other_schemes.local import local_delta
from random_allocation.comparisons.definitions import PrivacyParams, SchemeConfig, Direction

# Type aliases
NumericFunction = Callable[[float], float]

# ==================== Add ====================
def allocation_delta_decomposition_add_from_PLD(epsilon: float, num_steps: int, Poisson_PLD_obj: PrivacyLossDistribution) -> float:
    lambda_val = 1 - (1-1.0/num_steps)**num_steps
    # use one of two identical formulas to avoid numerical instability
    if epsilon < 1:
        lambda_new = lambda_val / (lambda_val + np.exp(epsilon)*(1-lambda_val))
    else:
        lambda_new = lambda_val*np.exp(-epsilon) / (lambda_val*np.exp(-epsilon) + (1-lambda_val))
    epsilon_new = -np.log(1-lambda_val*(1-np.exp(-epsilon)))
    return float(Poisson_PLD_obj.get_delta_for_epsilon(epsilon_new)/lambda_new)

def allocation_delta_decomposition_add(params: PrivacyParams,
                                       config: SchemeConfig,
                                       ) -> float:
    """Helper function to compute delta for the add direction in decomposition scheme"""
    if params.epsilon is None:
        raise ValueError("Epsilon must be provided to compute delta")
        
    num_steps_per_round = int(np.ceil(params.num_steps/params.num_selected))
    num_rounds = int(np.ceil(params.num_steps/num_steps_per_round))
    
    Poisson_PLD_obj = Poisson_PLD(
        sigma=params.sigma, 
        num_steps=num_steps_per_round, 
        num_epochs=num_rounds*params.num_epochs, 
        sampling_prob=1.0/num_steps_per_round, 
        discretization=config.discretization, 
        direction='add'
    )
    
    return allocation_delta_decomposition_add_from_PLD(
        epsilon=params.epsilon, 
        num_steps=num_steps_per_round,
        Poisson_PLD_obj=Poisson_PLD_obj
    )

def allocation_epsilon_decomposition_add(params: PrivacyParams,
                                         config: SchemeConfig,
                                         ) -> float:
    """Helper function to compute epsilon for the add direction in decomposition scheme"""
    if params.delta is None:
        raise ValueError("Delta must be provided to compute epsilon")
        
    num_steps_per_round = int(np.ceil(params.num_steps/params.num_selected))
    num_rounds = int(np.ceil(params.num_steps/num_steps_per_round))
    lambda_val = 1 - (1-1.0/num_steps_per_round)**num_steps_per_round
    
    Poisson_PLD_obj = Poisson_PLD(
        sigma=params.sigma, 
        num_steps=num_steps_per_round, 
        num_epochs=num_rounds*params.num_epochs, 
        sampling_prob=1.0/num_steps_per_round, 
        discretization=config.discretization, 
        direction='add'
    )
    
    optimization_func = lambda eps: float(Poisson_PLD_obj.get_delta_for_epsilon(-np.log(1-lambda_val*(1-np.exp(-eps)))))
    
    epsilon = search_function_with_bounds(
        func=optimization_func, 
        y_target=params.delta, 
        bounds=(0, config.epsilon_upper_bound),
        tolerance=config.epsilon_tolerance, 
        function_type=FunctionType.DECREASING
    )
    
    if epsilon is None:
        return float(np.inf)
    
    lower_bound = max(0, (epsilon-config.epsilon_tolerance)/2)
    upper_bound = min((epsilon + config.epsilon_tolerance)*2, config.epsilon_upper_bound)
    
    optimization_func = lambda eps: allocation_delta_decomposition_add_from_PLD(
        epsilon=eps, 
        num_steps=num_steps_per_round,
        Poisson_PLD_obj=Poisson_PLD_obj
    )
    
    epsilon = search_function_with_bounds(
        func=optimization_func, 
        y_target=params.delta, 
        bounds=(lower_bound, upper_bound),
        tolerance=config.epsilon_tolerance, 
        function_type=FunctionType.DECREASING
    )
    
    return float(np.inf) if epsilon is None else float(epsilon)

# ==================== Remove ====================
def allocation_delta_decomposition_remove(params: PrivacyParams,
                                          config: SchemeConfig,
                                          ) -> float:
    """Helper function to compute delta for the remove direction in decomposition scheme"""
    if params.epsilon is None:
        raise ValueError("Epsilon must be provided to compute delta")
        
    num_steps_per_round = int(np.ceil(params.num_steps/params.num_selected))
    num_rounds = int(np.ceil(params.num_steps/num_steps_per_round))
    lambda_val = 1 - (1-1.0/num_steps_per_round)**num_steps_per_round
    epsilon_new = np.log(1+lambda_val*(np.exp(params.epsilon)-1))
    
    Poisson_params = PrivacyParams(
        sigma=params.sigma, 
        epsilon=epsilon_new, 
        num_steps=num_steps_per_round, 
        num_selected=1, 
        num_epochs=num_rounds*params.num_epochs
    )
    delta_Poisson = Poisson_delta_PLD(params=Poisson_params, config=config)
    
    return float(delta_Poisson / lambda_val)

def allocation_epsilon_decomposition_remove(params: PrivacyParams,
                                            config: SchemeConfig,
                                            ) -> float:
    """Helper function to compute epsilon for the remove direction in decomposition scheme"""
    if params.delta is None:
        raise ValueError("Delta must be provided to compute epsilon")
        
    num_steps_per_round = int(np.ceil(params.num_steps/params.num_selected))
    num_rounds = int(np.ceil(params.num_steps/num_steps_per_round))
    lambda_val = 1 - (1-1.0/num_steps_per_round)**num_steps_per_round
    delta_new = params.delta * lambda_val
    
    Poisson_params = PrivacyParams(
        sigma=params.sigma, 
        delta=delta_new, 
        num_steps=num_steps_per_round, 
        num_selected=1, 
        num_epochs=num_rounds*params.num_epochs
    )

    epsilon_Poisson = Poisson_epsilon_PLD(params=Poisson_params, config=config)
    
    factor = 1.0/lambda_val
    # use one of two identical formulas to avoid numerical instability
    if epsilon_Poisson < 1:
        amplified_epsilon = np.log(1+factor*(np.exp(epsilon_Poisson)-1))
    else:
        amplified_epsilon = epsilon_Poisson + np.log(factor + (1-factor)*np.exp(-epsilon_Poisson))
    
    return float(amplified_epsilon)

# ==================== Both ====================
def allocation_epsilon_decomposition(params: PrivacyParams,
                                     config: SchemeConfig,
                                     direction: Direction = Direction.BOTH,
                                     ) -> float:
    """
    Compute epsilon for the decomposition allocation scheme.
    
    Args:
        params: Privacy parameters (must include delta)
        config: Scheme configuration parameters
        direction: The direction of privacy. Can be ADD, REMOVE, or BOTH.
    
    Returns:
        Computed epsilon value
    """
    params.validate()
    if params.delta is None:
        raise ValueError("Delta must be provided to compute epsilon")
        
    epsilon_remove: Optional[float] = None
    if direction != Direction.ADD:
        epsilon_remove = allocation_epsilon_decomposition_remove(params=params, config=config)
    
    epsilon_add: Optional[float] = None
    if direction != Direction.REMOVE:
        epsilon_add = allocation_epsilon_decomposition_add(params=params, config=config)
    
    if direction == Direction.ADD:
        assert epsilon_add is not None, "epsilon_add should be defined"
        return epsilon_add
    if direction == Direction.REMOVE:
        assert epsilon_remove is not None, "epsilon_remove should be defined"
        return epsilon_remove
        
    # Both directions - both should be defined
    assert epsilon_add is not None, "epsilon_add should be defined"
    assert epsilon_remove is not None, "epsilon_remove should be defined"
    return float(max(epsilon_remove, epsilon_add))

def allocation_delta_decomposition(params: PrivacyParams,
                                   config: SchemeConfig,
                                   direction: Direction = Direction.BOTH,
                                   ) -> float:
    """
    Compute delta for the decomposition allocation scheme.
    
    Args:
        params: Privacy parameters (must include epsilon)
        config: Scheme configuration parameters
        direction: The direction of privacy. Can be ADD, REMOVE, or BOTH.
    
    Returns:
        Computed delta value
    """
    params.validate()
    if params.epsilon is None:
        raise ValueError("Epsilon must be provided to compute delta")
    
    delta_remove: Optional[float] = None
    if direction != Direction.ADD:
        delta_remove = allocation_delta_decomposition_remove(params=params, config=config)
    
    delta_add: Optional[float] = None
    if direction != Direction.REMOVE:
        delta_add = allocation_delta_decomposition_add(params=params, config=config)
    
    if direction == Direction.ADD:
        assert delta_add is not None, "delta_add should be defined"
        return delta_add
    if direction == Direction.REMOVE:
        assert delta_remove is not None, "delta_remove should be defined"
        return delta_remove
    
    # Both directions - both should be defined
    assert delta_add is not None, "delta_add should be defined"
    assert delta_remove is not None, "delta_remove should be defined"
    return float(max(delta_add, delta_remove))
