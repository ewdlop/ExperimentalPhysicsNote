```python
import numpy as np
import scipy.constants as const
import matplotlib.pyplot as plt

class RadiationPhenomena:
    """
    Comprehensive analysis of Bremsstrahlung and Cyclotron Radiation
    """
    
    @staticmethod
    def bremsstrahlung_radiation(
        electron_energy=1e6,  # Electron energy in eV
        target_material='tungsten',
        electron_current=1e-3  # Amperes
    ):
        """
        Bremsstrahlung (Braking Radiation) Analysis
        
        Parameters:
        electron_energy (float): Electron beam energy
        target_material (str): Target material
        electron_current (float): Electron beam current
        
        Returns:
        dict: Bremsstrahlung radiation characteristics
        """
        # Material-specific properties
        material_properties = {
            'tungsten': {
                'atomic_number': 74,
                'density': 19.3,  # g/cm³
                'melting_point': 3422  # K
            },
            'copper': {
                'atomic_number': 29,
                'density': 8.96,  # g/cm³
                'melting_point': 1358  # K
            }
        }
        
        # Convert electron energy to Joules
        energy_joules = electron_energy * const.e
        
        # Bremsstrahlung spectrum generation
        def radiation_spectrum():
            """
            Generate simplified Bremsstrahlung spectrum
            """
            # Photon energy range
            max_photon_energy = energy_joules
            photon_energies = np.linspace(0, max_photon_energy, 200)
            
            # Simplified spectral distribution
            # Based on Kramers' approximation
            material = material_properties.get(
                target_material, 
                material_properties['tungsten']
            )
            
            # Spectral intensity approximation
            def spectral_intensity(E):
                """
                Compute spectral intensity of Bremsstrahlung
                """
                Z = material['atomic_number']
                return Z * (max_photon_energy - E) / max_photon_energy
            
            intensities = [spectral_intensity(E) for E in photon_energies]
            
            return {
                'photon_energies': photon_energies,
                'intensities': intensities
            }
        
        # Power calculation
        def radiation_power():
            """
            Compute total radiated power
            """
            # Simplified Larmor formula approximation
            material = material_properties.get(
                target_material, 
                material_properties['tungsten']
            )
            
            # Power calculation
            power = (
                2 * const.e**2 / (3 * const.c**2) * 
                material['atomic_number']**2 * 
                electron_current * 
                (energy_joules / const.e)**2
            )
            
            return power
        
        return {
            'electron_energy': electron_energy,
            'target_material': target_material,
            'radiation_spectrum': radiation_spectrum(),
            'total_radiated_power': radiation_power()
        }
    
    @staticmethod
    def cyclotron_radiation(
        particle_charge=const.e,  # Electron charge
        particle_mass=const.m_e,  # Electron mass
        magnetic_field_strength=1.0,  # Tesla
        particle_energy=1e6  # eV
    ):
        """
        Cyclotron Radiation Analysis
        
        Parameters:
        particle_charge (float): Particle charge
        particle_mass (float): Particle mass
        magnetic_field_strength (float): Magnetic field strength
        particle_energy (float): Particle energy
        
        Returns:
        dict: Cyclotron radiation characteristics
        """
        # Cyclotron frequency calculation
        def cyclotron_frequency():
            """
            Compute cyclotron frequency
            """
            return (
                particle_charge * magnetic_field_strength / 
                particle_mass
            )
        
        # Radiation characteristics
        def radiation_properties():
            """
            Compute radiation emission properties
            """
            # Gyroradius (Larmor radius)
            velocity = np.sqrt(
                2 * (particle_energy * const.e) / particle_mass
            )
            
            gyroradius = (
                particle_mass * velocity / 
                (particle_charge * magnetic_field_strength)
            )
            
            # Radiation power
            def radiation_power():
                """
                Compute synchrotron radiation power
                """
                return (
                    2 * const.e**2 * velocity**2 / 
                    (3 * const.c**2 * gyroradius**2)
                )
            
            return {
                'gyroradius': gyroradius,
                'velocity': velocity,
                'radiation_power': radiation_power()
            }
        
        # Radiation spectrum generation
        def radiation_spectrum():
            """
            Generate cyclotron radiation spectrum
            """
            # Fundamental and harmonic frequencies
            freq = cyclotron_frequency()
            harmonics = [freq * (n+1) for n in range(5)]
            
            # Simplified spectral intensity
            intensities = [1 / (n+1) for n in range(5)]
            
            return {
                'frequencies': harmonics,
                'intensities': intensities
            }
        
        return {
            'particle_charge': particle_charge,
            'magnetic_field_strength': magnetic_field_strength,
            'cyclotron_frequency': cyclotron_frequency(),
            'radiation_properties': radiation_properties(),
            'radiation_spectrum': radiation_spectrum()
        }
    
    def visualize_radiation_phenomena(self):
        """
        Visualize Bremsstrahlung and Cyclotron Radiation
        """
        plt.figure(figsize=(15, 6))
        
        # Bremsstrahlung Spectrum
        plt.subplot(121)
        bremss_results = self.bremsstrahlung_radiation()
        plt.plot(
            bremss_results['radiation_spectrum']['photon_energies'] / const.e,
            bremss_results['radiation_spectrum']['intensities']
        )
        plt.title('Bremsstrahlung Spectrum')
        plt.xlabel('Photon Energy (eV)')
        plt.ylabel('Intensity')
        
        # Cyclotron Radiation Spectrum
        plt.subplot(122)
        cyclotron_results = self.cyclotron_radiation()
        plt.bar(
            cyclotron_results['radiation_spectrum']['frequencies'],
            cyclotron_results['radiation_spectrum']['intensities']
        )
        plt.title('Cyclotron Radiation Spectrum')
        plt.xlabel('Frequency')
        plt.ylabel('Intensity')
        
        plt.tight_layout()
        plt.show()

def main():
    # Create radiation phenomena instance
    radiation_exp = RadiationPhenomena()
    
    # Bremsstrahlung Radiation Analysis
    print("Bremsstrahlung Radiation:")
    bremss_results = radiation_exp.bremsstrahlung_radiation()
    print(f"Total Radiated Power: {bremss_results['total_radiated_power']} W")
    
    # Cyclotron Radiation Analysis
    print("\nCyclotron Radiation:")
    cyclotron_results = radiation_exp.cyclotron_radiation()
    print(f"Cyclotron Frequency: {cyclotron_results['cyclotron_frequency']} Hz")
    
    # Visualize radiation phenomena
    radiation_exp.visualize_radiation_phenomena()

if __name__ == "__main__":
    main()
```
