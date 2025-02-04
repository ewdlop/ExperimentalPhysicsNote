import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List, Optional
from dataclasses import dataclass

@dataclass
class FourVector:
    """Represents a four-vector in spacetime (ct, x, y, z)"""
    ct: float  # Time component (multiplied by c)
    x: float   # x spatial component
    y: float   # y spatial component
    z: float   # z spatial component
    
    def __add__(self, other: 'FourVector') -> 'FourVector':
        return FourVector(
            self.ct + other.ct,
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )
    
    def proper_time(self) -> float:
        """Calculate proper time interval (invariant)"""
        return np.sqrt(self.ct**2 - self.x**2 - self.y**2 - self.z**2)

class SpecialRelativity:
    """Class for special relativity calculations"""
    
    def __init__(self):
        self.c = 299792458  # Speed of light in m/s
        
    def lorentz_factor(self, v: float) -> float:
        """
        Calculate Lorentz factor gamma
        
        Args:
            v: Velocity in m/s
            
        Returns:
            float: Lorentz factor
        """
        beta = v / self.c
        return 1 / np.sqrt(1 - beta**2)
    
    def time_dilation(self, proper_time: float, v: float) -> float:
        """
        Calculate dilated time in moving frame
        
        Args:
            proper_time: Time in rest frame (seconds)
            v: Relative velocity (m/s)
            
        Returns:
            float: Dilated time
        """
        gamma = self.lorentz_factor(v)
        return gamma * proper_time
    
    def length_contraction(self, proper_length: float, v: float) -> float:
        """
        Calculate contracted length in moving frame
        
        Args:
            proper_length: Length in rest frame (meters)
            v: Relative velocity (m/s)
            
        Returns:
            float: Contracted length
        """
        gamma = self.lorentz_factor(v)
        return proper_length / gamma
    
    def relativistic_mass(self, rest_mass: float, v: float) -> float:
        """
        Calculate relativistic mass
        
        Args:
            rest_mass: Mass in rest frame (kg)
            v: Velocity (m/s)
            
        Returns:
            float: Relativistic mass
        """
        gamma = self.lorentz_factor(v)
        return gamma * rest_mass
    
    def relativistic_momentum(self, mass: float, v: float) -> float:
        """
        Calculate relativistic momentum
        
        Args:
            mass: Rest mass (kg)
            v: Velocity (m/s)
            
        Returns:
            float: Relativistic momentum
        """
        gamma = self.lorentz_factor(v)
        return gamma * mass * v
    
    def relativistic_energy(self, mass: float, v: float) -> Tuple[float, float]:
        """
        Calculate total relativistic energy and kinetic energy
        
        Args:
            mass: Rest mass (kg)
            v: Velocity (m/s)
            
        Returns:
            Tuple[float, float]: (Total energy, Kinetic energy)
        """
        gamma = self.lorentz_factor(v)
        total_energy = gamma * mass * self.c**2
        kinetic_energy = total_energy - mass * self.c**2
        return total_energy, kinetic_energy
    
    def lorentz_transform(self, 
                         event: FourVector, 
                         v: float, 
                         direction: str = 'x') -> FourVector:
        """
        Perform Lorentz transformation on a spacetime event
        
        Args:
            event: FourVector representing the event
            v: Relative velocity between frames (m/s)
            direction: Direction of relative motion ('x', 'y', or 'z')
            
        Returns:
            FourVector: Transformed event coordinates
        """
        gamma = self.lorentz_factor(v)
        beta = v / self.c
        
        if direction == 'x':
            return FourVector(
                gamma * (event.ct - beta * event.x),
                gamma * (event.x - beta * event.ct),
                event.y,
                event.z
            )
        elif direction == 'y':
            return FourVector(
                gamma * (event.ct - beta * event.y),
                event.x,
                gamma * (event.y - beta * event.ct),
                event.z
            )
        elif direction == 'z':
            return FourVector(
                gamma * (event.ct - beta * event.z),
                event.x,
                event.y,
                gamma * (event.z - beta * event.ct)
            )
        else:
            raise ValueError("Direction must be 'x', 'y', or 'z'")

    def plot_worldline(self, 
                      events: List[FourVector],
                      v: float = 0,
                      title: str = "Worldline Diagram") -> None:
        """
        Plot worldline diagram for a series of events
        
        Args:
            events: List of events to plot
            v: Optional velocity for showing different reference frame
            title: Plot title
        """
        # Extract coordinates
        cts = [event.ct for event in events]
        xs = [event.x for event in events]
        
        # Create figure
        plt.figure(figsize=(10, 8))
        
        # Plot events in original frame
        plt.plot(xs, cts, 'b-', label='Original frame')
        plt.scatter(xs, cts, color='blue')
        
        if v != 0:
            # Transform events to moving frame
            transformed_events = [self.lorentz_transform(event, v) for event in events]
            transformed_cts = [event.ct for event in transformed_events]
            transformed_xs = [event.x for event in transformed_events]
            
            # Plot events in transformed frame
            plt.plot(transformed_xs, transformed_cts, 'r--', label=f'Frame moving at v={v:0.2e} m/s')
            plt.scatter(transformed_xs, transformed_cts, color='red')
        
        # Plot light cone
        max_ct = max(cts)
        x_light = np.linspace(-max_ct, max_ct, 100)
        plt.plot(x_light, x_light, 'k:', label='Light cone', alpha=0.5)
        plt.plot(x_light, -x_light, 'k:', alpha=0.5)
        
        plt.grid(True)
        plt.xlabel('x (meters)')
        plt.ylabel('ct (meter-seconds)')
        plt.title(title)
        plt.legend()
        plt.axis('equal')
        plt.show()

class RelativisticCollision:
    """Class for analyzing relativistic collisions"""
    
    def __init__(self, sr: SpecialRelativity):
        self.sr = sr
    
    def elastic_collision(self, 
                         m1: float, 
                         m2: float, 
                         v1: float, 
                         v2: float) -> Tuple[float, float]:
        """
        Calculate final velocities in elastic relativistic collision
        
        Args:
            m1, m2: Rest masses of particles (kg)
            v1, v2: Initial velocities (m/s)
            
        Returns:
            Tuple[float, float]: Final velocities
        """
        # Calculate initial momenta and energies
        p1 = self.sr.relativistic_momentum(m1, v1)
        p2 = self.sr.relativistic_momentum(m2, v2)
        E1, _ = self.sr.relativistic_energy(m1, v1)
        E2, _ = self.sr.relativistic_energy(m2, v2)
        
        # Conservation of momentum and energy gives system of equations
        # Solve numerically for final velocities
        def equations(v_final):
            v1f, v2f = v_final
            p1f = self.sr.relativistic_momentum(m1, v1f)
            p2f = self.sr.relativistic_momentum(m2, v2f)
            E1f, _ = self.sr.relativistic_energy(m1, v1f)
            E2f, _ = self.sr.relativistic_energy(m2, v2f)
            
            return [
                p1f + p2f - (p1 + p2),  # Conservation of momentum
                E1f + E2f - (E1 + E2)   # Conservation of energy
            ]
        
        # Use numerical solver to find final velocities
        from scipy.optimize import fsolve
        v1f, v2f = fsolve(equations, [0, 0])
        
        return v1f, v2f

def example_usage():
    """Example usage of special relativity calculations"""
    
    sr = SpecialRelativity()
    
    # Example 1: Time dilation
    proper_time = 1.0  # 1 second
    velocity = 0.8 * sr.c  # 80% speed of light
    dilated_time = sr.time_dilation(proper_time, velocity)
    print(f"Time dilation: {dilated_time:.2f} seconds")
    
    # Example 2: Length contraction
    proper_length = 1.0  # 1 meter
    contracted_length = sr.length_contraction(proper_length, velocity)
    print(f"Length contraction: {contracted_length:.2f} meters")
    
    # Example 3: Worldline plot
    events = [
        FourVector(0, 0, 0, 0),
        FourVector(1, 0.5, 0, 0),
        FourVector(2, 1.0, 0, 0),
        FourVector(3, 1.5, 0, 0)
    ]
    sr.plot_worldline(events, velocity, "Example Worldline")
    
    # Example 4: Relativistic collision
    collision = RelativisticCollision(sr)
    m1 = 1.0  # 1 kg
    m2 = 2.0  # 2 kg
    v1 = 0.6 * sr.c
    v2 = -0.3 * sr.c
    v1f, v2f = collision.elastic_collision(m1, m2, v1, v2)
    print(f"Collision final velocities: {v1f/sr.c:.2f}c, {v2f/sr.c:.2f}c")

if __name__ == "__main__":
    example_usage()
