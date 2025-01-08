import numpy as np
from scipy import constants
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum

class Direction(Enum):
    FORWARD = 1
    BACKWARD = -1

@dataclass
class Particle:
    """Represents a charged particle in the accelerator"""
    mass: float  # kg
    charge: float  # Coulombs
    position: np.ndarray  # [x, y, z] in meters
    momentum: np.ndarray  # [px, py, pz] in kg*m/s
    
    @property
    def energy(self) -> float:
        """Calculate total energy in GeV"""
        p_squared = np.sum(self.momentum**2)
        m_squared = self.mass**2
        return np.sqrt(p_squared * constants.c**2 + m_squared * constants.c**4) / constants.e / 1e9
    
    def reverse(self):
        """Reverse particle momentum for backward propagation"""
        self.momentum = -self.momentum

class AcceleratorComponent:
    """Base class for accelerator components with reversible fields"""
    def __init__(self, length: float):
        self.length = length  # meters
        
    def apply_field(self, particle: Particle, dt: float, direction: Direction, t: Optional[float] = None):
        """Apply fields to particle, handling both forward and backward propagation"""
        raise NotImplementedError

class QuadrupoleMagnet(AcceleratorComponent):
    """Simulates a quadrupole magnet for beam focusing"""
    def __init__(self, length: float, gradient: float):
        super().__init__(length)
        self.gradient = gradient  # Tesla/meter
        
    def apply_field(self, particle: Particle, dt: float, direction: Direction, t: Optional[float] = None):
        """Apply quadrupole magnetic field with directional support"""
        x, y, _ = particle.position
        
        # Quadrupole field components (Bx = gy, By = gx)
        # Field direction remains the same, but particle motion is reversed
        Bx = self.gradient * y
        By = self.gradient * x
        
        # Lorentz force (direction.value = ±1 handles propagation direction)
        force = direction.value * particle.charge * np.cross(
            particle.momentum/particle.mass,
            np.array([Bx, By, 0])
        )
        
        # Update momentum
        particle.momentum += force * dt
        
        # Update position (direction already encoded in momentum)
        particle.position += (particle.momentum / particle.mass) * dt

class SuperconductingMagnet(AcceleratorComponent):
    """Simulates a superconducting dipole magnet for beam steering"""
    def __init__(self, length: float, field_strength: float):
        super().__init__(length)
        self.field_strength = field_strength  # Tesla
        
    def apply_field(self, particle: Particle, dt: float, direction: Direction, t: Optional[float] = None):
        """Apply uniform magnetic field with directional support"""
        # Uniform vertical magnetic field
        B = np.array([0, self.field_strength, 0])
        
        # Lorentz force with direction
        force = direction.value * particle.charge * np.cross(
            particle.momentum/particle.mass,
            B
        )
        
        # Update momentum
        particle.momentum += force * dt
        
        # Update position
        particle.position += (particle.momentum / particle.mass) * dt

class RFCavity(AcceleratorComponent):
    """Simulates an RF cavity for particle acceleration"""
    def __init__(self, length: float, frequency: float, voltage: float, phase: float):
        super().__init__(length)
        self.frequency = frequency  # Hz
        self.voltage = voltage  # Volts
        self.phase = phase  # radians
        
    def apply_field(self, particle: Particle, dt: float, direction: Direction, t: Optional[float] = None):
        """Apply RF electric field with directional support"""
        if t is None:
            raise ValueError("Time parameter required for RF cavity")
            
        z = particle.position[2]
        
        # For backward propagation, we need to adjust the phase
        t_effective = t if direction == Direction.FORWARD else -t
        
        # Standing wave with direction-dependent phase
        Ez = self.voltage * np.sin(2*np.pi*self.frequency*t_effective + self.phase) * \
             np.sin(np.pi*z/self.length)
        
        # Electric force with direction
        force = np.array([0, 0, direction.value * particle.charge * Ez])
        
        # Update momentum
        particle.momentum += force * dt
        
        # Update position
        particle.position += (particle.momentum / particle.mass) * dt

class AcceleratorSimulation:
    """Main simulation class for particle tracking with reversible propagation"""
    def __init__(self):
        self.components = []
        self.particles = []
        self.time = 0
        self.direction = Direction.FORWARD
        
    def add_component(self, component: AcceleratorComponent):
        """Add accelerator component to beamline"""
        self.components.append(component)
        
    def add_particle(self, particle: Particle):
        """Add particle to simulation"""
        self.particles.append(particle)
    
    def reverse_direction(self):
        """Switch propagation direction and reverse particle momenta"""
        self.direction = Direction.BACKWARD if self.direction == Direction.FORWARD else Direction.FORWARD
        for particle in self.particles:
            particle.reverse()
        
    def step(self, dt: float):
        """Advance simulation by time step dt in current direction"""
        dt_effective = dt * self.direction.value
        
        for component in self.components:
            for particle in self.particles:
                if isinstance(component, RFCavity):
                    component.apply_field(particle, dt, self.direction, self.time)
                else:
                    component.apply_field(particle, dt, self.direction)
                    
        self.time += dt_effective

def run_backward_tracking_example():
    """Example of backward tracking from desired end state"""
    # Create simulation
    sim = AcceleratorSimulation()
    
    # Add components (in reverse order for backward tracking)
    sim.add_component(RFCavity(length=1.0, frequency=1e9, voltage=5e6, phase=0))
    sim.add_component(SuperconductingMagnet(length=2.0, field_strength=5))
    sim.add_component(QuadrupoleMagnet(length=0.5, gradient=10))
    
    # Add test particle at desired final state
    proton = Particle(
        mass=constants.proton_mass,
        charge=constants.elementary_charge,
        position=np.array([0.0, 0.0, 5.0]),  # Desired end position
        momentum=np.array([0, 0, 2e-20])     # Desired end momentum
    )
    sim.add_particle(proton)
    
    # Set to backward propagation
    sim.reverse_direction()
    
    # Run simulation backwards
    dt = 1e-11  # 10 picoseconds
    steps = 1000
    
    trajectory = []
    energies = []
    
    for _ in range(steps):
        sim.step(dt)
        trajectory.append(proton.position.copy())
        energies.append(proton.energy)
    
    return np.array(trajectory), np.array(energies)

if __name__ == "__main__":
    # Run backward tracking example
    trajectory, energies = run_backward_tracking_example()
    
    # Print results
    print(f"Initial particle energy (found by backward tracking): {energies[-1]:.2f} GeV")
    print(f"Required injection position: {trajectory[-1]}")
    print(f"Maximum deviation from axis: {np.max(np.abs(trajectory[:,:2])):.2e} m")
