"""
F1 Pit Stop Strategy Recommender
Rekomendasi strategi pit stop lengkap: jumlah pit, compound per stint, timing pit stop
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class StintPlan:
    """Rencana stint dengan compound dan lap range"""
    stint_number: int
    compound: str
    start_lap: int
    end_lap: int
    total_laps: int
    pit_after_lap: int  # Lap untuk pit stop (0 jika stint terakhir)

@dataclass
class PitStopStrategy:
    """Strategy pit stop lengkap untuk satu race"""
    strategy_name: str  # "One-Stop", "Two-Stop", "Three-Stop"
    total_pit_stops: int
    stint_plans: List[StintPlan]
    estimated_race_time: float  # Estimasi waktu race (seconds)
    risk_level: str  # "Low", "Medium", "High"
    confidence_score: float
    reasoning: str

class F1PitStopStrategyEngine:
    """Engine untuk generate strategi pit stop optimal"""
    
    def __init__(self):
        # Tire compound characteristics
        self.compound_degradation = {
            'SOFT': 0.08,      # Degradasi per lap (8%)
            'MEDIUM': 0.05,    # (5%)
            'HARD': 0.03,      # (3%)
            'INTERMEDIATE': 0.06,
            'WET': 0.07
        }
        
        self.compound_pace = {
            'SOFT': 1.0,       # Pace baseline (fastest)
            'MEDIUM': 0.97,    # 0.3s slower per lap
            'HARD': 0.94,      # 0.6s slower per lap
            'INTERMEDIATE': 0.92,
            'WET': 0.88
        }
        
        self.compound_max_laps = {
            'SOFT': {'low': 25, 'medium': 20, 'high': 15},
            'MEDIUM': {'low': 40, 'medium': 30, 'high': 25},
            'HARD': {'low': 55, 'medium': 45, 'high': 35},
            'INTERMEDIATE': {'low': 30, 'medium': 25, 'high': 20},
            'WET': {'low': 35, 'medium': 30, 'high': 25}
        }
        
        # Pit stop time loss (seconds)
        self.pit_stop_time_loss = 22  # ~20s pit + 2s in/out lap loss
    
    def generate_strategies(self, 
                          total_race_laps: int,
                          track_temp: float,
                          air_temp: float,
                          tyre_severity: str,  # 'low', 'medium', 'high'
                          rainfall: bool
                          ) -> List[PitStopStrategy]:
        """
        Generate multiple pit stop strategy options
        
        Returns list of strategies ranked by confidence
        """
        strategies = []
        
        # Determine available compounds based on conditions
        if rainfall:
            # Wet conditions - simple strategy
            strategies.append(self._generate_wet_strategy(total_race_laps, tyre_severity))
            return strategies
        
        # Dry conditions - generate multiple strategies
        # Always generate all 3 strategies for comparison
        
        # 1. ONE-STOP STRATEGY
        one_stop = self._generate_one_stop(
            total_race_laps, track_temp, air_temp, tyre_severity
        )
        if one_stop:
            strategies.append(one_stop)
        
        # 2. TWO-STOP STRATEGY
        two_stop = self._generate_two_stop(
            total_race_laps, track_temp, air_temp, tyre_severity
        )
        if two_stop:
            strategies.append(two_stop)
        
        # 3. THREE-STOP STRATEGY (aggressive)
        three_stop = self._generate_three_stop(
            total_race_laps, track_temp, air_temp, tyre_severity
        )
        if three_stop:
            strategies.append(three_stop)
        
        # Sort by confidence score
        strategies.sort(key=lambda x: x.confidence_score, reverse=True)
        
        return strategies
    
    def _generate_one_stop(self, total_laps, track_temp, air_temp, severity) -> PitStopStrategy:
        """Generate optimal one-stop strategy"""
        
        # More sensitive compound selection based on temperature
        avg_temp = (track_temp + air_temp) / 2
        
        if track_temp < 25:
            # Very cold - SOFT start essential for grip
            stint1_compound = 'SOFT'
            stint2_compound = 'MEDIUM'
        elif track_temp < 32:
            # Cool - SOFT to MEDIUM
            stint1_compound = 'SOFT'
            stint2_compound = 'MEDIUM' if severity != 'high' else 'HARD'
        elif track_temp < 40:
            # Moderate - MEDIUM compounds
            stint1_compound = 'MEDIUM'
            stint2_compound = 'HARD' if severity == 'high' else 'MEDIUM'
        elif track_temp < 48:
            # Warm - MEDIUM to HARD
            stint1_compound = 'MEDIUM'
            stint2_compound = 'HARD'
        else:
            # Very hot - HARD compounds needed
            stint1_compound = 'HARD' if severity == 'high' else 'MEDIUM'
            stint2_compound = 'HARD'
        
        # Calculate pit stop timing - varies by severity
        max_laps_stint1 = self.compound_max_laps[stint1_compound][severity]
        
        # Pit stop timing varies by severity
        if severity == 'low':
            optimal_pit_lap = int(total_laps * 0.45)  # Later pit, tyres last longer
        elif severity == 'high':
            optimal_pit_lap = int(total_laps * 0.35)  # Earlier pit, more degradation
        else:
            optimal_pit_lap = int(total_laps * 0.40)  # Standard timing
        
        # Adjust based on compound limits
        if optimal_pit_lap > max_laps_stint1:
            optimal_pit_lap = max_laps_stint1 - 2  # Safety margin
        
        stint1_laps = optimal_pit_lap
        stint2_laps = total_laps - optimal_pit_lap
        
        # Check if stint 2 is feasible
        max_laps_stint2 = self.compound_max_laps[stint2_compound][severity]
        if stint2_laps > max_laps_stint2:
            # Not feasible
            return None
        
        # Create stint plans
        stint_plans = [
            StintPlan(
                stint_number=1,
                compound=stint1_compound,
                start_lap=1,
                end_lap=optimal_pit_lap,
                total_laps=stint1_laps,
                pit_after_lap=optimal_pit_lap
            ),
            StintPlan(
                stint_number=2,
                compound=stint2_compound,
                start_lap=optimal_pit_lap + 1,
                end_lap=total_laps,
                total_laps=stint2_laps,
                pit_after_lap=0
            )
        ]
        
        # Calculate estimated race time
        estimated_time = self._calculate_race_time(stint_plans, 1)
        
        # Determine risk level
        if stint2_laps > max_laps_stint2 * 0.9:
            risk = "High"
            confidence = 0.70
        elif stint2_laps > max_laps_stint2 * 0.8:
            risk = "Medium"
            confidence = 0.85
        else:
            risk = "Low"
            confidence = 0.90
        
        reasoning = f"Start on {stint1_compound}, pit lap {optimal_pit_lap}, finish on {stint2_compound}. "
        reasoning += f"Conservative strategy with {1} pit stop. "
        reasoning += f"Stint 2: {stint2_laps} laps on {stint2_compound} (max: {max_laps_stint2})."
        
        return PitStopStrategy(
            strategy_name="One-Stop Strategy",
            total_pit_stops=1,
            stint_plans=stint_plans,
            estimated_race_time=estimated_time,
            risk_level=risk,
            confidence_score=confidence,
            reasoning=reasoning
        )
    
    def _generate_two_stop(self, total_laps, track_temp, air_temp, severity) -> PitStopStrategy:
        """Generate optimal two-stop strategy"""
        
        # More granular compound selection
        if track_temp < 25:
            # Very cold - All SOFT for grip
            compounds = ['SOFT', 'SOFT', 'SOFT']
        elif track_temp < 32:
            # Cool - SOFT dominant
            compounds = ['SOFT', 'SOFT', 'MEDIUM']
        elif track_temp < 40:
            # Moderate - Mixed strategy
            if severity == 'high':
                compounds = ['SOFT', 'MEDIUM', 'HARD']
            else:
                compounds = ['SOFT', 'MEDIUM', 'SOFT']
        elif track_temp < 48:
            # Warm - MEDIUM/HARD mix
            if severity == 'high':
                compounds = ['MEDIUM', 'HARD', 'HARD']
            else:
                compounds = ['MEDIUM', 'MEDIUM', 'HARD']
        else:
            # Very hot - HARD dominant
            compounds = ['MEDIUM', 'HARD', 'HARD']
        
        # Calculate pit timing
        # First pit: ~25-30% of race
        # Second pit: ~55-65% of race
        pit1_lap = int(total_laps * 0.28)
        pit2_lap = int(total_laps * 0.60)
        
        # Adjust based on compound limits
        max_laps_c1 = self.compound_max_laps[compounds[0]][severity]
        max_laps_c2 = self.compound_max_laps[compounds[1]][severity]
        max_laps_c3 = self.compound_max_laps[compounds[2]][severity]
        
        if pit1_lap > max_laps_c1:
            pit1_lap = max_laps_c1 - 2
        
        stint2_laps = pit2_lap - pit1_lap
        if stint2_laps > max_laps_c2:
            pit2_lap = pit1_lap + max_laps_c2 - 2
        
        stint3_laps = total_laps - pit2_lap
        if stint3_laps > max_laps_c3:
            # Not feasible
            return None
        
        # Create stint plans
        stint_plans = [
            StintPlan(1, compounds[0], 1, pit1_lap, pit1_lap, pit1_lap),
            StintPlan(2, compounds[1], pit1_lap + 1, pit2_lap, pit2_lap - pit1_lap, pit2_lap),
            StintPlan(3, compounds[2], pit2_lap + 1, total_laps, total_laps - pit2_lap, 0)
        ]
        
        estimated_time = self._calculate_race_time(stint_plans, 2)
        
        # Two-stop usually lower risk (fresher tyres)
        risk = "Medium"
        confidence = 0.88
        
        reasoning = f"Aggressive two-stop: {compounds[0]} (lap 1-{pit1_lap}), "
        reasoning += f"{compounds[1]} (lap {pit1_lap+1}-{pit2_lap}), "
        reasoning += f"{compounds[2]} (lap {pit2_lap+1}-{total_laps}). "
        reasoning += f"Pit stops at lap {pit1_lap} and {pit2_lap}."
        
        return PitStopStrategy(
            strategy_name="Two-Stop Strategy",
            total_pit_stops=2,
            stint_plans=stint_plans,
            estimated_race_time=estimated_time,
            risk_level=risk,
            confidence_score=confidence,
            reasoning=reasoning
        )
    
    def _generate_three_stop(self, total_laps, track_temp, air_temp, severity) -> PitStopStrategy:
        """Generate aggressive three-stop strategy"""
        
        # Very aggressive - maximize pace with fresh tyres
        if track_temp < 25:
            # Very cold - All SOFT for maximum pace
            compounds = ['SOFT', 'SOFT', 'SOFT', 'SOFT']
        elif track_temp < 32:
            # Cool - SOFT heavy
            compounds = ['SOFT', 'SOFT', 'SOFT', 'MEDIUM']
        elif track_temp < 40:
            # Moderate - Balanced aggression
            if severity == 'high':
                compounds = ['SOFT', 'MEDIUM', 'MEDIUM', 'HARD']
            else:
                compounds = ['SOFT', 'MEDIUM', 'SOFT', 'MEDIUM']
        elif track_temp < 48:
            # Warm - MEDIUM dominant
            compounds = ['SOFT', 'MEDIUM', 'MEDIUM', 'HARD']
        else:
            # Very hot - Need durability
            compounds = ['MEDIUM', 'MEDIUM', 'HARD', 'HARD']
        
        # Pit timings: ~20%, ~40%, ~65%
        pit1_lap = int(total_laps * 0.22)
        pit2_lap = int(total_laps * 0.43)
        pit3_lap = int(total_laps * 0.68)
        
        stint_plans = [
            StintPlan(1, compounds[0], 1, pit1_lap, pit1_lap, pit1_lap),
            StintPlan(2, compounds[1], pit1_lap + 1, pit2_lap, pit2_lap - pit1_lap, pit2_lap),
            StintPlan(3, compounds[2], pit2_lap + 1, pit3_lap, pit3_lap - pit2_lap, pit3_lap),
            StintPlan(4, compounds[3], pit3_lap + 1, total_laps, total_laps - pit3_lap, 0)
        ]
        
        estimated_time = self._calculate_race_time(stint_plans, 3)
        
        risk = "High"
        confidence = 0.72
        
        reasoning = f"Very aggressive three-stop for maximum pace. "
        reasoning += f"Pits at lap {pit1_lap}, {pit2_lap}, and {pit3_lap}. "
        reasoning += f"Sequence: {' → '.join(compounds)}. "
        reasoning += "Requires clean air and no safety cars."
        
        return PitStopStrategy(
            strategy_name="Three-Stop Strategy",
            total_pit_stops=3,
            stint_plans=stint_plans,
            estimated_race_time=estimated_time,
            risk_level=risk,
            confidence_score=confidence,
            reasoning=reasoning
        )
    
    def _generate_wet_strategy(self, total_laps, severity) -> PitStopStrategy:
        """Generate strategy for wet conditions"""
        
        # Simple wet strategy - INTERMEDIATE throughout or WET if heavy rain
        compounds = ['INTERMEDIATE']
        
        # Check if need pit for WET tyres
        max_laps = self.compound_max_laps['INTERMEDIATE'][severity]
        
        if total_laps <= max_laps:
            # No stop strategy
            stint_plans = [
                StintPlan(1, 'INTERMEDIATE', 1, total_laps, total_laps, 0)
            ]
            pit_stops = 0
            strategy_name = "No-Stop Strategy (Wet)"
        else:
            # One stop - INTERMEDIATE to INTERMEDIATE or WET
            pit_lap = int(total_laps * 0.50)
            stint_plans = [
                StintPlan(1, 'INTERMEDIATE', 1, pit_lap, pit_lap, pit_lap),
                StintPlan(2, 'INTERMEDIATE', pit_lap + 1, total_laps, total_laps - pit_lap, 0)
            ]
            pit_stops = 1
            strategy_name = "One-Stop Strategy (Wet)"
        
        estimated_time = self._calculate_race_time(stint_plans, pit_stops)
        
        reasoning = "Wet conditions detected. Strategy adapts to changing weather. "
        reasoning += "Monitor track conditions for potential switch to slicks."
        
        return PitStopStrategy(
            strategy_name=strategy_name,
            total_pit_stops=pit_stops,
            stint_plans=stint_plans,
            estimated_race_time=estimated_time,
            risk_level="Medium",
            confidence_score=0.80,
            reasoning=reasoning
        )
    
    def _calculate_race_time(self, stint_plans: List[StintPlan], num_pit_stops: int) -> float:
        """Calculate estimated race time in seconds"""
        
        # Base lap time (assume 90 seconds average)
        base_lap_time = 90.0
        total_time = 0.0
        
        for stint in stint_plans:
            compound = stint.compound
            pace_factor = self.compound_pace[compound]
            deg_rate = self.compound_degradation[compound]
            
            # Calculate time for this stint with degradation
            for lap in range(stint.total_laps):
                # Degradation increases lap time
                degradation_penalty = deg_rate * lap * 0.1  # 0.1s per lap per % degradation
                lap_time = (base_lap_time / pace_factor) + degradation_penalty
                total_time += lap_time
        
        # Add pit stop time
        total_time += num_pit_stops * self.pit_stop_time_loss
        
        return total_time


def format_strategy_output(strategy: PitStopStrategy) -> str:
    """Format strategy for display"""
    
    output = f"\n{'='*80}\n"
    output += f"🏁 {strategy.strategy_name.upper()}\n"
    output += f"{'='*80}\n\n"
    
    output += f"📊 Overview:\n"
    output += f"   • Total Pit Stops: {strategy.total_pit_stops}\n"
    output += f"   • Risk Level: {strategy.risk_level}\n"
    output += f"   • Confidence: {strategy.confidence_score*100:.1f}%\n"
    output += f"   • Est. Race Time: {strategy.estimated_race_time//60:.0f}m {strategy.estimated_race_time%60:.0f}s\n\n"
    
    output += f"🔧 Stint Breakdown:\n"
    for stint in strategy.stint_plans:
        output += f"\n   Stint {stint.stint_number}: {stint.compound}\n"
        output += f"      Laps: {stint.start_lap} → {stint.end_lap} ({stint.total_laps} laps)\n"
        if stint.pit_after_lap > 0:
            output += f"      ⛽ PIT STOP after lap {stint.pit_after_lap}\n"
    
    output += f"\n💡 Strategy Reasoning:\n"
    output += f"   {strategy.reasoning}\n"
    
    output += f"\n{'='*80}\n"
    
    return output


# Example usage
if __name__ == "__main__":
    engine = F1PitStopStrategyEngine()
    
    # Example race conditions
    strategies = engine.generate_strategies(
        total_race_laps=58,
        track_temp=35,
        air_temp=28,
        tyre_severity='medium',
        rainfall=False
    )
    
    print("\n🏎️ F1 PIT STOP STRATEGY RECOMMENDATIONS")
    print(f"Race: 58 laps | Track: 35°C | Severity: Medium")
    
    for i, strategy in enumerate(strategies, 1):
        print(f"\n{'#'*80}")
        print(f"OPTION {i} - Confidence: {strategy.confidence_score*100:.1f}%")
        print(format_strategy_output(strategy))
