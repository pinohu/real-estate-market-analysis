"""
Negotiation Strategy Generator for Real Estate Valuation and Negotiation Strategist

This module generates tailored negotiation strategies and scripts based on property analysis,
market conditions, and seller motivation factors.
"""

import os
import json
import random
from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import pandas as pd
from datetime import datetime

class SellerMotivationAnalyzer:
    """
    Analyzes seller motivation based on property and market data
    """
    
    def __init__(self):
        """Initialize the SellerMotivationAnalyzer"""
        pass
        
    def analyze_motivation(self, property_data: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes seller motivation based on property and market data
        
        Args:
            property_data: Property details and characteristics
            market_data: Market analysis and conditions
            
        Returns:
            Dict containing seller motivation assessment
        """
        # Extract relevant data
        days_on_market = property_data.get('days_on_market', 
                                          market_data.get('market_metrics', {}).get('days_on_market', 30))
        
        listing_status = property_data.get('listing_status', 'For Sale')
        if listing_status != 'For Sale':
            # If not for sale, use default market metrics
            days_on_market = market_data.get('market_metrics', {}).get('days_on_market', 30)
        
        # Determine if there have been price cuts
        original_list_price = property_data.get('original_list_price', None)
        current_price = property_data.get('listing_price', property_data.get('estimated_value', 0))
        
        # If original list price is not available, estimate it
        if original_list_price is None:
            # Randomly determine if there were price cuts
            has_price_cuts = random.random() < 0.3  # 30% chance of price cuts
            
            if has_price_cuts:
                # Estimate original price 5-15% higher than current
                original_list_price = current_price * (1 + random.uniform(0.05, 0.15))
            else:
                original_list_price = current_price
        
        price_cuts = 0
        price_reduction_pct = 0
        
        if original_list_price > current_price:
            price_reduction_pct = (original_list_price - current_price) / original_list_price * 100
            
            # Estimate number of price cuts based on reduction percentage
            if price_reduction_pct > 10:
                price_cuts = random.choice([2, 3])
            elif price_reduction_pct > 5:
                price_cuts = random.choice([1, 2])
            elif price_reduction_pct > 0:
                price_cuts = 1
        
        # Extract market data
        market_type = market_data.get('supply_demand', {}).get('market_type', 'balanced')
        market_cycle = market_data.get('market_cycle', {}).get('cycle_position', 'Expansion')
        avg_dom = market_data.get('market_metrics', {}).get('days_on_market', 30)
        
        # Determine base motivation score (0-100)
        motivation_score = 50  # Start with neutral motivation
        
        # Adjust based on days on market
        if days_on_market > avg_dom * 2:
            motivation_score += 25  # Significantly above average DOM
        elif days_on_market > avg_dom * 1.5:
            motivation_score += 15  # Above average DOM
        elif days_on_market > avg_dom:
            motivation_score += 5   # Slightly above average DOM
        elif days_on_market < avg_dom * 0.5:
            motivation_score -= 15  # Significantly below average DOM
        
        # Adjust based on price cuts
        if price_cuts >= 2:
            motivation_score += 20  # Multiple price cuts
        elif price_cuts == 1:
            motivation_score += 10  # One price cut
        
        # Adjust based on price reduction percentage
        if price_reduction_pct > 10:
            motivation_score += 20  # Significant price reduction
        elif price_reduction_pct > 5:
            motivation_score += 10  # Moderate price reduction
        
        # Adjust based on market conditions
        if market_type == 'buyer':
            motivation_score += 15  # Buyer's market increases motivation
        elif market_type == 'seller':
            motivation_score -= 15  # Seller's market decreases motivation
            
        if market_cycle in ['Early Contraction', 'Contraction']:
            motivation_score += 10  # Declining market increases motivation
        elif market_cycle == 'Expansion':
            motivation_score -= 10  # Rising market decreases motivation
        
        # Cap the score between 0 and 100
        motivation_score = max(0, min(100, motivation_score))
        
        # Determine motivation level
        if motivation_score >= 75:
            motivation_level = 'high'
        elif motivation_score >= 40:
            motivation_level = 'moderate'
        else:
            motivation_level = 'low'
        
        # Identify potential motivation factors
        motivation_factors = []
        
        if days_on_market > avg_dom:
            motivation_factors.append(f"Property has been on market for {days_on_market} days (market average: {avg_dom})")
        
        if price_cuts > 0:
            motivation_factors.append(f"{price_cuts} price reduction(s) totaling {price_reduction_pct:.1f}% of original list price")
        
        if market_type == 'buyer':
            motivation_factors.append("Current buyer's market conditions")
        
        if market_cycle in ['Early Contraction', 'Contraction']:
            motivation_factors.append(f"Declining market in {market_cycle} phase")
        
        # Add seasonal factors if relevant
        current_month = datetime.now().month
        if current_month in [11, 12, 1, 2]:  # Winter months
            motivation_factors.append("Winter season typically has fewer buyers")
        
        # If we don't have enough factors, add some generic possibilities
        if len(motivation_factors) < 2:
            possible_factors = [
                "Possible life change (job relocation, divorce, etc.)",
                "May have already purchased another home",
                "Potential financial pressure",
                "Property may have been inherited",
                "Possible investment property liquidation"
            ]
            
            # Add some random factors based on motivation level
            if motivation_level == 'high':
                motivation_factors.extend(random.sample(possible_factors, min(2, len(possible_factors))))
            elif motivation_level == 'moderate' and len(motivation_factors) < 2:
                motivation_factors.append(random.choice(possible_factors))
        
        # Calculate carrying costs
        carrying_costs = self._estimate_carrying_costs(property_data)
        
        return {
            'score': motivation_score,
            'level': motivation_level,
            'factors': motivation_factors,
            'days_on_market': days_on_market,
            'price_cuts': price_cuts,
            'price_reduction_pct': round(price_reduction_pct, 1),
            'carrying_costs': carrying_costs
        }
    
    def _estimate_carrying_costs(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Estimates monthly carrying costs for the seller
        
        Args:
            property_data: Property details
            
        Returns:
            Dict containing estimated carrying costs
        """
        # Extract property value
        property_value = property_data.get('estimated_value', 500000)
        
        # Estimate mortgage payment (assuming 80% LTV, 30-year fixed at 5.5%)
        loan_amount = property_value * 0.8
        interest_rate = 0.055
        monthly_rate = interest_rate / 12
        term_months = 30 * 12
        
        mortgage_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** term_months) / ((1 + monthly_rate) ** term_months - 1)
        
        # Estimate property tax (annual rate of 1% divided by 12)
        property_tax = property_data.get('annual_tax_amount', property_value * 0.01) / 12
        
        # Estimate insurance (annual rate of 0.5% divided by 12)
        insurance = property_value * 0.005 / 12
        
        # Estimate utilities and maintenance
        utilities = 200  # Flat estimate
        maintenance = property_value * 0.01 / 12  # 1% of value annually for maintenance
        
        # Calculate total monthly carrying cost
        total_monthly = mortgage_payment + property_tax + insurance + utilities + maintenance
        
        # Calculate opportunity cost (assuming 4% annual return on equity)
        equity = property_value * 0.2  # Assuming 20% equity
        opportunity_cost = equity * 0.04 / 12
        
        return {
            'mortgage': round(mortgage_payment),
            'property_tax': round(property_tax),
            'insurance': round(insurance),
            'utilities': utilities,
            'maintenance': round(maintenance),
            'total_monthly': round(total_monthly),
            'opportunity_cost': round(opportunity_cost),
            'total_monthly_with_opportunity': round(total_monthly + opportunity_cost),
            'cost_per_additional_month': round(total_monthly + opportunity_cost)
        }


class BuyerLeverageAnalyzer:
    """
    Identifies leverage points for the buyer in negotiations
    """
    
    def __init__(self):
        """Initialize the BuyerLeverageAnalyzer"""
        pass
        
    def identify_leverage(self, 
                         property_data: Dict[str, Any], 
                         valuation_data: Dict[str, Any], 
                         market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identifies leverage points for the buyer in negotiations
        
        Args:
            property_data: Property details and characteristics
            valuation_data: Property valuation and investment analysis
            market_data: Market analysis and conditions
            
        Returns:
            Dict containing buyer leverage points
        """
        leverage_points = []
        leverage_score = 50  # Start with neutral leverage
        
        # Extract key data
        listing_price = property_data.get('listing_price', property_data.get('estimated_value', 0))
        estimated_value = valuation_data.get('valuation', {}).get('final_value', 0)
        days_on_market = property_data.get('days_on_market', 0)
        avg_dom = market_data.get('market_metrics', {}).get('days_on_market', 30)
        market_type = market_data.get('supply_demand', {}).get('market_type', 'balanced')
        property_condition = valuation_data.get('renovation_analysis', {}).get('property_condition', 'Good')
        
        # Check for price leverage
        if listing_price > estimated_value * 1.05:
            leverage_points.append({
                'type': 'price',
                'description': 'Property is overpriced compared to estimated value',
                'strength': 'high',
                'negotiation_impact': f"Potential {round((listing_price - estimated_value) / listing_price * 100, 1)}% price reduction opportunity"
            })
            leverage_score += 15
        elif listing_price > estimated_value * 1.02:
            leverage_points.append({
                'type': 'price',
                'description': 'Property is slightly overpriced compared to estimated value',
                'strength': 'moderate',
                'negotiation_impact': f"Potential {round((listing_price - estimated_value) / listing_price * 100, 1)}% price reduction opportunity"
            })
            leverage_score += 5
        
        # Check for time on market leverage
        if days_on_market > avg_dom * 2:
            leverage_points.append({
                'type': 'time',
                'description': f'Property has been on the market for {days_on_market} days (more than double the average)',
                'strength': 'high',
                'negotiation_impact': 'Seller likely experiencing market fatigue and carrying costs'
            })
            leverage_score += 15
        elif days_on_market > avg_dom:
            leverage_points.append({
                'type': 'time',
                'description': f'Property has been on the market for {days_on_market} days (above average)',
                'strength': 'moderate',
                'negotiation_impact': 'Seller may be becoming concerned about selling timeline'
            })
            leverage_score += 10
        
        # Check for market condition leverage
        if market_type == 'buyer':
            leverage_points.append({
                'type': 'market',
                'description': 'Current market favors buyers',
                'strength': 'high',
                'negotiation_impact': 'Reduced competition and more negotiating power'
            })
            leverage_score += 15
        elif market_type == 'balanced':
            leverage_points.append({
                'type': 'market',
                'description': 'Market is balanced between buyers and sellers',
                'strength': 'moderate',
                'negotiation_impact': 'Fair negotiation environment with reasonable flexibility'
            })
            leverage_score += 5
        
        # Check for property condition leverage
        if property_condition in ['Poor', 'Fair']:
            leverage_points.append({
                'type': 'condition',
                'description': f'Property is in {property_condition} condition',
                'strength': 'high',
                'negotiation_impact': 'Repairs and renovations needed, justifying lower offer'
            })
            leverage_score += 15
        elif property_condition == 'Good':
            leverage_points.append({
                'type': 'condition',
                'description': 'Property is in good condition but may need some updates',
                'strength': 'low',
                'negotiation_impact': 'Minor improvements needed, potential for small concessions'
            })
            leverage_score += 5
        
        # Check for investment metrics leverage
        investment_metrics = valuation_data.get('investment_metrics', {})
        cash_flow = investment_metrics.get('financing_scenarios', {}).get('twenty_percent_down', {}).get('monthly_cash_flow', 0)
        
        if cash_flow < 0:
            leverage_points.append({
                'type': 'investment',
                'description': 'Property has negative cash flow at current price',
                'strength': 'high',
                'negotiation_impact': 'Price reduction needed to achieve positive cash flow'
            })
            leverage_score += 10
        
        # Check for renovation leverage
        renovation_analysis = valuation_data.get('renovation_analysis', {})
        renovation_cost = renovation_analysis.get('estimated_renovation_cost', 0)
        
        if renovation_cost > property_value * 0.1:
            leverage_points.append({
                'type': 'renovation',
                'description': f'Property needs significant renovations (estimated ${renovation_cost:,})',
                'strength': 'high',
                'negotiation_impact': 'Renovation costs justify lower purchase price or seller credits'
            })
            leverage_score += 10
        elif renovation_cost > property_value * 0.05:
            leverage_points.append({
                'type': 'renovation',
                'description': f'Property needs moderate renovations (estimated ${renovation_cost:,})',
                'strength': 'moderate',
                'negotiation_impact': 'Renovation costs justify modest price reduction or seller credits'
            })
            leverage_score += 5
        
        # Cap the score between 0 and 100
        leverage_score = max(0, min(100, leverage_score))
        
        # Determine overall leverage level
        if leverage_score >= 75:
            leverage_level = 'high'
        elif leverage_score >= 40:
            leverage_level = 'moderate'
        else:
            leverage_level = 'low'
        
        return {
            'score': leverage_score,
            'level': leverage_level,
            'points': leverage_points,
            'primary_leverage': leverage_points[0] if leverage_points else None,
            'secondary_leverage': leverage_points[1] if len(leverage_points) > 1 else None
        }


class StrategyGenerator:
    """
    Generates negotiation strategies based on property analysis and market conditions
    """
    
    def __init__(self):
        """Initialize the StrategyGenerator"""
        self.seller_motivation_analyzer = SellerMotivationAnalyzer()
        self.buyer_leverage_analyzer = BuyerLeverageAnalyzer()
        
    def generate_strategies(self, 
                           property_data: Dict[str, Any], 
                           market_data: Dict[str, Any], 
                           valuation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates tailored negotiation strategies based on property, valuation, and market data
        
        Args:
            property_data: Property details and characteristics
            market_data: Market analysis and conditions
            valuation_data: Property valuation and investment analysis
            
        Returns:
            Dict containing recommended negotiation strategies and their projected impacts
        """
        try:
            # Analyze seller motivation
            seller_motivation = self.seller_motivation_analyzer.analyze_motivation(property_data, market_data)
            
            # Identify buyer leverage points
            buyer_leverage = self.buyer_leverage_analyzer.identify_leverage(property_data, valuation_data, market_data)
            
            # Generate price negotiation strategies
            price_strategies = self._generate_price_strategies(property_data, valuation_data, market_data, seller_motivation)
            
            # Generate terms negotiation strategies
            terms_strategies = self._generate_terms_strategies(property_data, valuation_data, market_data, seller_motivation)
            
            # Generate creative negotiation strategies
            creative_strategies = self._generate_creative_strategies(property_data, valuation_data, market_data, seller_motivation)
            
            # Calculate ROI impact for each strategy
            strategies_with_roi = self._calculate_roi_impact(
                price_strategies + terms_strategies + creative_strategies,
                valuation_data
            )
            
            # Rank strategies by effectiveness and acceptability
            ranked_strategies = self._rank_strategies(
                strategies_with_roi,
                seller_motivation,
                market_data
            )
            
            # Create final recommendation package
            recommendation = {
                'success': True,
                'seller_motivation': seller_motivation,
                'buyer_leverage': buyer_leverage,
                'recommended_strategies': ranked_strategies,
                'negotiation_script': self._generate_negotiation_script(ranked_strategies[0] if ranked_strategies else None),
                'fallback_options': self._identify_fallback_options(ranked_strategies)
            }
            
            return recommendation
            
        except Exception as e:
            return {
                'success': False,
                'error': 'Failed to generate negotiation strategies',
                'error_message': str(e)
            }
    
    def _generate_price_strategies(self, 
                                  property_data: Dict[str, Any], 
                                  valuation_data: Dict[str, Any], 
                                  market_data: Dict[str, Any], 
                                  seller_motivation: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generates price-based negotiation strategies
        
        Args:
            property_data: Property details
            valuation_data: Property valuation data
            market_data: Market analysis data
            seller_motivation: Seller motivation assessment
            
        Returns:
            List of price-based negotiation strategies
        """
        strategies = []
        
        # Extract key data
        listing_price = property_data.get('listing_price', property_data.get('estimated_value', 0))
        estimated_value = valuation_data.get('valuation', {}).get('final_value', 0)
        motivation_level = seller_motivation.get('level', 'moderate')
        market_type = market_data.get('supply_demand', {}).get('market_type', 'balanced')
        days_on_market = property_data.get('days_on_market', 0)
        avg_dom = market_data.get('market_metrics', {}).get('days_on_market', 30)
        
        # Strategy 1: Below-market offer with justification
        discount_pct = 0
        
        if motivation_level == 'high':
            discount_pct = 0.12 if market_type == 'buyer' else 0.08
        elif motivation_level == 'moderate':
            discount_pct = 0.08 if market_type == 'buyer' else 0.05
        else:  # low motivation
            discount_pct = 0.05 if market_type == 'buyer' else 0.03
        
        # Adjust discount based on days on market
        if days_on_market > avg_dom * 2:
            discount_pct += 0.03
        elif days_on_market > avg_dom:
            discount_pct += 0.01
        
        # Calculate offer price
        offer_price = int(listing_price * (1 - discount_pct))
        
        # Create justification based on property and market factors
        justifications = []
        
        if listing_price > estimated_value:
            justifications.append(f"Property is overpriced by ${listing_price - estimated_value:,} based on our valuation")
        
        if days_on_market > avg_dom:
            justifications.append(f"Property has been on the market for {days_on_market} days (above average)")
        
        property_condition = valuation_data.get('renovation_analysis', {}).get('property_condition', 'Good')
        if property_condition in ['Poor', 'Fair']:
            renovation_cost = valuation_data.get('renovation_analysis', {}).get('estimated_renovation_cost', 0)
            justifications.append(f"Property requires approximately ${renovation_cost:,} in renovations")
        
        # Add strategy
        strategies.append({
            'type': 'price',
            'name': 'Below-Market Offer with Justification',
            'description': f"Make an offer of ${offer_price:,} (approximately {discount_pct*100:.1f}% below listing price)",
            'justification': justifications,
            'offer_price': offer_price,
            'discount_percentage': round(discount_pct * 100, 1),
            'expected_success_probability': self._calculate_success_probability(discount_pct, motivation_level, market_type)
        })
        
        # Strategy 2: Incremental negotiation approach
        initial_discount_pct = discount_pct * 0.7  # Start with smaller discount
        initial_offer_price = int(listing_price * (1 - initial_discount_pct))
        
        strategies.append({
            'type': 'price',
            'name': 'Incremental Negotiation Approach',
            'description': f"Start with an offer of ${initial_offer_price:,} and be prepared to increase in small increments",
            'justification': ["Starting with a reasonable offer allows room for back-and-forth negotiation",
                             "Shows willingness to work with seller while still achieving a good price"],
            'offer_price': initial_offer_price,
            'discount_percentage': round(initial_discount_pct * 100, 1),
            'max_price': int(listing_price * (1 - discount_pct * 0.3)),  # Maximum price willing to pay
            'increment_size': int(listing_price * 0.01),  # 1% increments
            'expected_success_probability': self._calculate_success_probability(initial_discount_pct * 0.8, motivation_level, market_type)
        })
        
        # Strategy 3: Conditional price tiers
        base_discount_pct = discount_pct * 0.9
        base_offer_price = int(listing_price * (1 - base_discount_pct))
        
        # Create conditional tiers
        condition_tiers = [
            {
                'condition': 'As-is purchase with no inspection contingency',
                'price': int(listing_price * (1 - base_discount_pct * 1.2))
            },
            {
                'condition': 'Quick closing (21 days or less)',
                'price': int(listing_price * (1 - base_discount_pct * 1.1))
            },
            {
                'condition': 'Standard terms with inspection contingency',
                'price': base_offer_price
            }
        ]
        
        strategies.append({
            'type': 'price',
            'name': 'Conditional Price Tiers',
            'description': f"Offer different prices based on conditions that benefit the seller",
            'justification': ["Gives seller options and control in the negotiation",
                             "Links price directly to terms that have value to both parties"],
            'base_offer_price': base_offer_price,
            'discount_percentage': round(base_discount_pct * 100, 1),
            'condition_tiers': condition_tiers,
            'expected_success_probability': self._calculate_success_probability(base_discount_pct * 0.9, motivation_level, market_type)
        })
        
        return strategies
    
    def _generate_terms_strategies(self, 
                                  property_data: Dict[str, Any], 
                                  valuation_data: Dict[str, Any], 
                                  market_data: Dict[str, Any], 
                                  seller_motivation: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generates terms-based negotiation strategies
        
        Args:
            property_data: Property details
            valuation_data: Property valuation data
            market_data: Market analysis data
            seller_motivation: Seller motivation assessment
            
        Returns:
            List of terms-based negotiation strategies
        """
        strategies = []
        
        # Extract key data
        listing_price = property_data.get('listing_price', property_data.get('estimated_value', 0))
        motivation_level = seller_motivation.get('level', 'moderate')
        motivation_factors = seller_motivation.get('factors', [])
        carrying_costs = seller_motivation.get('carrying_costs', {}).get('total_monthly_with_opportunity', 0)
        
        # Strategy 1: Closing timeline flexibility
        if any("already purchased" in factor.lower() for factor in motivation_factors):
            # Seller may have already purchased another home
            strategies.append({
                'type': 'terms',
                'name': 'Closing Timeline Flexibility',
                'description': "Offer flexible closing timeline to accommodate seller's needs",
                'justification': ["Seller may have already purchased another home and needs specific timing",
                                 "Flexibility on closing date can be more valuable than price for some sellers"],
                'options': [
                    {'name': 'Quick closing', 'description': 'Close in 14-21 days'},
                    {'name': 'Delayed closing', 'description': 'Allow seller to stay in property for 30-60 days after closing'},
                    {'name': 'Rent-back option', 'description': 'Allow seller to rent the property back for a specified period'}
                ],
                'price_impact': 'Minimal',
                'expected_success_probability': 0.8 if motivation_level == 'high' else 0.7 if motivation_level == 'moderate' else 0.5
            })
        else:
            # General closing timeline strategy
            strategies.append({
                'type': 'terms',
                'name': 'Closing Timeline Flexibility',
                'description': "Offer to close on seller's preferred timeline",
                'justification': ["Accommodating seller's timeline can be more valuable than a slightly higher offer",
                                 f"Each month of carrying costs for seller is approximately ${carrying_costs:,}"],
                'options': [
                    {'name': 'Quick closing', 'description': 'Close in 14-21 days'},
                    {'name': 'Standard closing', 'description': 'Close in 30-45 days'},
                    {'name': 'Extended closing', 'description': 'Close in 60+ days if seller needs time'}
                ],
                'price_impact': 'Can justify 1-2% lower offer price for quick closing',
                'expected_success_probability': 0.7 if motivation_level == 'high' else 0.6 if motivation_level == 'moderate' else 0.5
            })
        
        # Strategy 2: Contingency adjustments
        strategies.append({
            'type': 'terms',
            'name': 'Contingency Adjustments',
            'description': "Modify or waive certain contingencies to strengthen offer",
            'justification': ["Reducing contingencies decreases risk for the seller",
                             "Creates cleaner offer that's more likely to close without issues"],
            'options': [
                {'name': 'Shorten inspection period', 'description': 'Complete inspection within 5-7 days instead of standard 10-14'},
                {'name': 'Limit inspection requests', 'description': 'Only request repairs for major issues exceeding $1,000'},
                {'name': 'Waive appraisal contingency', 'description': 'Agree to cover gap if appraisal comes in low (with cap)'},
                {'name': 'As-is purchase', 'description': 'Waive inspection contingency entirely (only if property condition is good)'}
            ],
            'price_impact': 'Can justify 1-3% higher offer price depending on contingencies waived',
            'expected_success_probability': 0.75 if motivation_level == 'high' else 0.65 if motivation_level == 'moderate' else 0.55
        })
        
        # Strategy 3: Earnest money optimization
        standard_earnest = listing_price * 0.01  # Standard is typically 1%
        increased_earnest = listing_price * 0.03  # Increased to 3%
        
        strategies.append({
            'type': 'terms',
            'name': 'Earnest Money Optimization',
            'description': f"Offer increased earnest money deposit of ${increased_earnest:,} (3% of listing price)",
            'justification': ["Larger earnest money demonstrates financial strength and seriousness",
                             "Provides seller with greater confidence in buyer's commitment"],
            'standard_amount': int(standard_earnest),
            'increased_amount': int(increased_earnest),
            'price_impact': 'Can justify 0.5-1% lower offer price',
            'expected_success_probability': 0.7 if motivation_level == 'high' else 0.6 if motivation_level == 'moderate' else 0.5
        })
        
        return strategies
    
    def _generate_creative_strategies(self, 
                                     property_data: Dict[str, Any], 
                                     valuation_data: Dict[str, Any], 
                                     market_data: Dict[str, Any], 
                                     seller_motivation: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generates creative negotiation strategies
        
        Args:
            property_data: Property details
            valuation_data: Property valuation data
            market_data: Market analysis data
            seller_motivation: Seller motivation assessment
            
        Returns:
            List of creative negotiation strategies
        """
        strategies = []
        
        # Extract key data
        listing_price = property_data.get('listing_price', property_data.get('estimated_value', 0))
        motivation_level = seller_motivation.get('level', 'moderate')
        property_condition = valuation_data.get('renovation_analysis', {}).get('property_condition', 'Good')
        renovation_cost = valuation_data.get('renovation_analysis', {}).get('estimated_renovation_cost', 0)
        
        # Strategy 1: Repair credits vs. price reductions
        if property_condition in ['Poor', 'Fair'] and renovation_cost > 0:
            strategies.append({
                'type': 'creative',
                'name': 'Repair Credits Instead of Price Reduction',
                'description': f"Request ${min(renovation_cost, listing_price*0.05):,} in repair credits instead of equivalent price reduction",
                'justification': ["Seller may prefer giving repair credits over reducing price",
                                 "Maintains higher recorded sale price which benefits neighborhood comps",
                                 "May have tax advantages for both parties"],
                'credit_amount': int(min(renovation_cost, listing_price*0.05)),
                'price_impact': 'Neutral - shifts price reduction to credits',
                'expected_success_probability': 0.8 if motivation_level == 'high' else 0.7 if motivation_level == 'moderate' else 0.5
            })
        
        # Strategy 2: As-is purchase with documented issues
        if property_condition in ['Poor', 'Fair']:
            strategies.append({
                'type': 'creative',
                'name': 'As-Is Purchase with Documented Issues',
                'description': "Offer to purchase property as-is after documenting issues through inspection",
                'justification': ["Eliminates repair negotiations but accounts for issues in initial offer price",
                                 "Provides clean, simple transaction for seller with no surprises",
                                 "Reduces seller's risk of deal falling through due to inspection issues"],
                'discount_needed': int(renovation_cost * 1.2),  # 20% buffer for unknown issues
                'process': [
                    "Conduct inspection for information only (not for negotiation)",
                    "Document all issues thoroughly",
                    "Make as-is offer with price accounting for documented issues"
                ],
                'price_impact': f"Justifies ${int(renovation_cost*1.2):,} reduction from listing price",
                'expected_success_probability': 0.75 if motivation_level == 'high' else 0.65 if motivation_level == 'moderate' else 0.45
            })
        
        # Strategy 3: Seller pain point solutions
        strategies.append({
            'type': 'creative',
            'name': 'Seller Pain Point Solutions',
            'description': "Identify and address specific seller pain points beyond price",
            'justification': ["Solving specific problems for the seller can be more valuable than price alone",
                             "Creates win-win scenario by addressing seller's unique needs"],
            'potential_solutions': [
                {'pain_point': 'Moving logistics', 'solution': 'Offer to cover moving expenses (up to $3,000)'},
                {'pain_point': 'Timing concerns', 'solution': 'Offer leaseback option at below-market rate'},
                {'pain_point': 'Unwanted items', 'solution': 'Agree to take furniture or other items seller doesn\'t want'},
                {'pain_point': 'Closing costs', 'solution': 'Offer to cover certain seller closing costs'}
            ],
            'price_impact': 'Can justify 1-2% higher offer price',
            'expected_success_probability': 0.8 if motivation_level == 'high' else 0.7 if motivation_level == 'moderate' else 0.5
        })
        
        # Strategy 4: Seller financing options (for high motivation sellers)
        if motivation_level == 'high':
            strategies.append({
                'type': 'creative',
                'name': 'Seller Financing Option',
                'description': "Propose seller financing for portion of purchase price",
                'justification': ["Provides seller with ongoing income stream",
                                 "Can offer higher interest rate than seller would get from bank deposits",
                                 "May allow for higher overall purchase price"],
                'structure': {
                    'down_payment': int(listing_price * 0.2),
                    'bank_financing': int(listing_price * 0.6),
                    'seller_financing': int(listing_price * 0.2),
                    'seller_note_terms': '5-year term at 6% interest with balloon payment',
                    'monthly_payment_to_seller': int((listing_price * 0.2) * 0.06 / 12)
                },
                'price_impact': 'Can justify 1-3% higher offer price',
                'expected_success_probability': 0.6 if motivation_level == 'high' else 0.3 if motivation_level == 'moderate' else 0.1
            })
        
        return strategies
    
    def _calculate_roi_impact(self, 
                             strategies: List[Dict[str, Any]], 
                             valuation_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Calculates ROI impact for each strategy
        
        Args:
            strategies: List of negotiation strategies
            valuation_data: Property valuation data
            
        Returns:
            List of strategies with ROI impact calculations
        """
        # Extract key financial data
        property_value = valuation_data.get('valuation', {}).get('final_value', 0)
        listing_price = valuation_data.get('valuation', {}).get('listing_price', property_value)
        
        # Get baseline investment metrics
        baseline_metrics = valuation_data.get('investment_metrics', {})
        baseline_cash_on_cash = baseline_metrics.get('financing_scenarios', {}).get('twenty_percent_down', {}).get('cash_on_cash_return', 0)
        baseline_cap_rate = baseline_metrics.get('rental_analysis', {}).get('cap_rate', 0)
        
        # Calculate ROI impact for each strategy
        for strategy in strategies:
            # Initialize ROI impact
            roi_impact = {
                'purchase_price_impact': 0,
                'cash_on_cash_impact': 0,
                'cap_rate_impact': 0,
                'total_savings': 0,
                'monthly_cash_flow_impact': 0
            }
            
            # Calculate price impact based on strategy type and details
            if strategy['type'] == 'price':
                if 'offer_price' in strategy:
                    price_reduction = listing_price - strategy['offer_price']
                    roi_impact['purchase_price_impact'] = -round(price_reduction / listing_price * 100, 1)
                    roi_impact['total_savings'] = price_reduction
                    
                    # Estimate cash flow impact (rough approximation)
                    monthly_payment_reduction = price_reduction * 0.8 * 0.06 / 12  # Assuming 80% LTV, 6% interest
                    roi_impact['monthly_cash_flow_impact'] = monthly_payment_reduction
                    
                    # Estimate cash-on-cash return impact
                    down_payment_reduction = price_reduction * 0.2  # Assuming 20% down
                    annual_cash_flow_increase = monthly_payment_reduction * 12
                    new_down_payment = (listing_price - price_reduction) * 0.2
                    
                    if new_down_payment > 0:
                        new_cash_on_cash = baseline_cash_on_cash + (annual_cash_flow_increase / new_down_payment * 100)
                        roi_impact['cash_on_cash_impact'] = round(new_cash_on_cash - baseline_cash_on_cash, 2)
                    
                    # Estimate cap rate impact
                    annual_expense_reduction = monthly_payment_reduction * 12
                    new_cap_rate = baseline_cap_rate + (annual_expense_reduction / (listing_price - price_reduction) * 100)
                    roi_impact['cap_rate_impact'] = round(new_cap_rate - baseline_cap_rate, 2)
            
            elif strategy['type'] == 'terms':
                # Terms strategies have more variable impacts
                if 'Closing Timeline' in strategy['name']:
                    if 'quick closing' in strategy['description'].lower():
                        # Quick closing might save 1 month of carrying costs
                        carrying_costs_saved = 3000  # Estimate
                        roi_impact['total_savings'] = carrying_costs_saved
                        roi_impact['purchase_price_impact'] = -1  # Assume 1% price reduction
                        roi_impact['monthly_cash_flow_impact'] = carrying_costs_saved / 12
                
                elif 'Contingency' in strategy['name']:
                    # Contingency adjustments might allow for slightly lower price
                    roi_impact['purchase_price_impact'] = -0.5  # Assume 0.5% price reduction
                    roi_impact['total_savings'] = listing_price * 0.005
                    roi_impact['monthly_cash_flow_impact'] = (listing_price * 0.005 * 0.8 * 0.06) / 12
                
                elif 'Earnest Money' in strategy['name']:
                    # Earnest money optimization might allow for slightly lower price
                    roi_impact['purchase_price_impact'] = -0.5  # Assume 0.5% price reduction
                    roi_impact['total_savings'] = listing_price * 0.005
                    roi_impact['monthly_cash_flow_impact'] = (listing_price * 0.005 * 0.8 * 0.06) / 12
            
            elif strategy['type'] == 'creative':
                if 'Repair Credits' in strategy['name'] and 'credit_amount' in strategy:
                    credit_amount = strategy['credit_amount']
                    roi_impact['total_savings'] = credit_amount
                    roi_impact['purchase_price_impact'] = 0  # Price stays the same
                    roi_impact['monthly_cash_flow_impact'] = 0  # Cash flow impact is minimal
                
                elif 'As-Is Purchase' in strategy['name'] and 'discount_needed' in strategy:
                    discount = strategy['discount_needed']
                    roi_impact['total_savings'] = discount
                    roi_impact['purchase_price_impact'] = -round(discount / listing_price * 100, 1)
                    roi_impact['monthly_cash_flow_impact'] = (discount * 0.8 * 0.06) / 12
                
                elif 'Seller Pain Point' in strategy['name']:
                    # Solving pain points might cost money but allow for lower price
                    cost_to_buyer = 2000  # Estimate
                    price_reduction = listing_price * 0.01  # Assume 1% price reduction
                    roi_impact['total_savings'] = price_reduction - cost_to_buyer
                    roi_impact['purchase_price_impact'] = -1  # 1% price reduction
                    roi_impact['monthly_cash_flow_impact'] = ((price_reduction - cost_to_buyer) * 0.8 * 0.06) / 12
                
                elif 'Seller Financing' in strategy['name'] and 'structure' in strategy:
                    # Seller financing might allow for better terms
                    seller_financing = strategy['structure']['seller_financing']
                    bank_financing = strategy['structure']['bank_financing']
                    
                    # Assume seller financing at 6% vs bank at 6.5%
                    interest_savings = seller_financing * (0.065 - 0.06)
                    roi_impact['total_savings'] = interest_savings
                    roi_impact['purchase_price_impact'] = 0  # Price stays the same
                    roi_impact['monthly_cash_flow_impact'] = interest_savings / 12
            
            # Calculate cash-on-cash and cap rate impacts if not already calculated
            if roi_impact['cash_on_cash_impact'] == 0 and roi_impact['monthly_cash_flow_impact'] > 0:
                annual_cash_flow_increase = roi_impact['monthly_cash_flow_impact'] * 12
                down_payment = listing_price * (1 + roi_impact['purchase_price_impact']/100) * 0.2
                
                if down_payment > 0:
                    roi_impact['cash_on_cash_impact'] = round(annual_cash_flow_increase / down_payment * 100, 2)
            
            if roi_impact['cap_rate_impact'] == 0 and roi_impact['monthly_cash_flow_impact'] > 0:
                annual_expense_reduction = roi_impact['monthly_cash_flow_impact'] * 12
                new_price = listing_price * (1 + roi_impact['purchase_price_impact']/100)
                
                if new_price > 0:
                    roi_impact['cap_rate_impact'] = round(annual_expense_reduction / new_price * 100, 2)
            
            # Add ROI impact to strategy
            strategy['roi_impact'] = roi_impact
        
        return strategies
    
    def _rank_strategies(self, 
                        strategies: List[Dict[str, Any]], 
                        seller_motivation: Dict[str, Any], 
                        market_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Ranks strategies by effectiveness and acceptability
        
        Args:
            strategies: List of negotiation strategies with ROI impact
            seller_motivation: Seller motivation assessment
            market_data: Market analysis data
            
        Returns:
            List of ranked strategies
        """
        # Extract key data
        motivation_level = seller_motivation.get('level', 'moderate')
        market_type = market_data.get('supply_demand', {}).get('market_type', 'balanced')
        
        # Calculate strategy scores
        for strategy in strategies:
            # Base score starts at 50
            score = 50
            
            # Add points for ROI impact
            roi_impact = strategy.get('roi_impact', {})
            total_savings = roi_impact.get('total_savings', 0)
            cash_on_cash_impact = roi_impact.get('cash_on_cash_impact', 0)
            
            # More savings = higher score
            if total_savings > 10000:
                score += 20
            elif total_savings > 5000:
                score += 10
            elif total_savings > 1000:
                score += 5
            
            # Better cash-on-cash return = higher score
            if cash_on_cash_impact > 2:
                score += 15
            elif cash_on_cash_impact > 1:
                score += 10
            elif cash_on_cash_impact > 0.5:
                score += 5
            
            # Add points for success probability
            success_probability = strategy.get('expected_success_probability', 0.5)
            score += success_probability * 30  # Up to 30 points for high probability
            
            # Adjust based on market conditions and seller motivation
            if market_type == 'buyer':
                # In buyer's market, price strategies get bonus
                if strategy['type'] == 'price':
                    score += 10
            elif market_type == 'seller':
                # In seller's market, terms and creative strategies get bonus
                if strategy['type'] in ['terms', 'creative']:
                    score += 10
            
            if motivation_level == 'high':
                # With highly motivated seller, price strategies get bonus
                if strategy['type'] == 'price':
                    score += 15
            elif motivation_level == 'low':
                # With low motivation seller, terms and creative strategies get bonus
                if strategy['type'] in ['terms', 'creative']:
                    score += 15
            
            # Add score to strategy
            strategy['score'] = score
        
        # Rank strategies by score
        ranked_strategies = sorted(strategies, key=lambda x: x.get('score', 0), reverse=True)
        
        # Add rank to each strategy
        for i, strategy in enumerate(ranked_strategies):
            strategy['rank'] = i + 1
        
        return ranked_strategies
    
    def _generate_negotiation_script(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a negotiation script based on the top strategy
        
        Args:
            strategy: Top-ranked negotiation strategy
            
        Returns:
            Dict containing negotiation script
        """
        if not strategy:
            return {
                'opening_statement': "I'm interested in this property and would like to discuss making an offer.",
                'key_points': ["Discuss property features", "Ask about seller's timeline", "Mention financing pre-approval"],
                'closing_statement': "I'll prepare a formal offer based on our discussion."
            }
        
        # Generate script based on strategy type
        if strategy['type'] == 'price':
            return self._generate_price_strategy_script(strategy)
        elif strategy['type'] == 'terms':
            return self._generate_terms_strategy_script(strategy)
        elif strategy['type'] == 'creative':
            return self._generate_creative_strategy_script(strategy)
        else:
            return {
                'opening_statement': "I'm interested in this property and would like to discuss making an offer.",
                'key_points': ["Discuss property features", "Ask about seller's timeline", "Mention financing pre-approval"],
                'closing_statement': "I'll prepare a formal offer based on our discussion."
            }
    
    def _generate_price_strategy_script(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a negotiation script for a price-based strategy
        
        Args:
            strategy: Price-based negotiation strategy
            
        Returns:
            Dict containing negotiation script
        """
        # Extract key data
        strategy_name = strategy.get('name', '')
        offer_price = strategy.get('offer_price', 0)
        justifications = strategy.get('justification', [])
        
        # Generate script based on strategy name
        if 'Below-Market Offer' in strategy_name:
            opening = f"After carefully analyzing the property and current market conditions, I'd like to make an offer of ${offer_price:,}."
            
            key_points = [
                "I've done extensive research on comparable properties in the area",
                f"My offer reflects {', '.join(justifications)}" if justifications else "My offer reflects current market conditions"
            ]
            
            if 'roi_impact' in strategy:
                savings = strategy['roi_impact'].get('total_savings', 0)
                key_points.append(f"This price point works with my investment criteria and budget constraints")
            
            closing = "I'm prepared to move forward quickly with this offer and can provide proof of funds or pre-approval."
            
        elif 'Incremental Negotiation' in strategy_name:
            opening = f"I'd like to start the conversation with an offer of ${offer_price:,}, though I understand we may need to discuss the price further."
            
            key_points = [
                "I'm flexible and open to finding a price that works for both of us",
                "I value clear communication throughout the negotiation process",
                "My initial offer is based on my analysis of the property and market"
            ]
            
            max_price = strategy.get('max_price', offer_price * 1.05)
            closing = f"While ${offer_price:,} is my starting point, I'm willing to work with you to find a mutually acceptable price. My absolute maximum budget for this property would be around ${max_price:,}."
            
        elif 'Conditional Price Tiers' in strategy_name:
            opening = "I'd like to propose a flexible pricing structure based on different terms that might be valuable to you."
            
            tiers = strategy.get('condition_tiers', [])
            key_points = [f"Option {i+1}: {tier['condition']} - ${tier['price']:,}" for i, tier in enumerate(tiers)]
            
            closing = "These options give you flexibility to choose what works best for your situation. I'm happy to discuss any of these approaches in more detail."
            
        else:
            # Generic price strategy script
            opening = f"I'd like to make an offer of ${offer_price:,} for the property."
            
            key_points = [
                "This offer is based on my careful analysis of the property and market",
                "I'm pre-approved for financing and ready to move forward",
                "I can be flexible on closing timeline to accommodate your needs"
            ]
            
            closing = "I look forward to your response and am open to discussing the details further."
        
        return {
            'opening_statement': opening,
            'key_points': key_points,
            'closing_statement': closing
        }
    
    def _generate_terms_strategy_script(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a negotiation script for a terms-based strategy
        
        Args:
            strategy: Terms-based negotiation strategy
            
        Returns:
            Dict containing negotiation script
        """
        # Extract key data
        strategy_name = strategy.get('name', '')
        description = strategy.get('description', '')
        justifications = strategy.get('justification', [])
        
        # Generate script based on strategy name
        if 'Closing Timeline' in strategy_name:
            opening = "I understand that timing can be as important as price in real estate transactions. I'd like to discuss how we can structure the closing timeline to best meet your needs."
            
            options = strategy.get('options', [])
            key_points = [f"Option: {option['name']} - {option['description']}" for option in options]
            
            if justifications:
                key_points.append(f"I'm offering this flexibility because {justifications[0].lower()}")
            
            closing = "By accommodating your preferred timeline, we can create a smoother transaction process for both of us. What timeline would work best for you?"
            
        elif 'Contingency' in strategy_name:
            opening = "To strengthen my offer, I'm willing to adjust the standard contingencies to reduce uncertainty for you as the seller."
            
            options = strategy.get('options', [])
            key_points = [f"I can {option['description'].lower()}" for option in options]
            
            if justifications:
                key_points.append(f"These adjustments benefit you because {justifications[0].lower()}")
            
            closing = "These modifications to standard contingencies demonstrate my serious interest in the property and confidence in completing the purchase."
            
        elif 'Earnest Money' in strategy_name:
            standard = strategy.get('standard_amount', 0)
            increased = strategy.get('increased_amount', 0)
            
            opening = f"To demonstrate my serious interest and financial capability, I'm prepared to offer an increased earnest money deposit of ${increased:,} instead of the standard ${standard:,}."
            
            key_points = [
                "This larger deposit shows my commitment to completing the purchase",
                "It provides you with greater security in accepting my offer",
                "I'm confident in my financing and ability to close"
            ]
            
            closing = "The increased earnest money deposit demonstrates that I'm a serious buyer with the financial means to complete this transaction smoothly."
            
        else:
            # Generic terms strategy script
            opening = "I'd like to discuss some flexible terms that might make my offer more attractive to you beyond just the price."
            
            key_points = [
                "I can be flexible on closing timeline to accommodate your needs",
                "I'm willing to work with you on contingencies to reduce uncertainty",
                "My goal is to create a smooth transaction process for both of us"
            ]
            
            closing = "By focusing on these terms, we can create a win-win agreement that addresses both our needs."
        
        return {
            'opening_statement': opening,
            'key_points': key_points,
            'closing_statement': closing
        }
    
    def _generate_creative_strategy_script(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates a negotiation script for a creative strategy
        
        Args:
            strategy: Creative negotiation strategy
            
        Returns:
            Dict containing negotiation script
        """
        # Extract key data
        strategy_name = strategy.get('name', '')
        description = strategy.get('description', '')
        justifications = strategy.get('justification', [])
        
        # Generate script based on strategy name
        if 'Repair Credits' in strategy_name:
            credit_amount = strategy.get('credit_amount', 0)
            
            opening = f"Rather than requesting a price reduction, I'd like to propose ${credit_amount:,} in repair credits to address some issues with the property."
            
            key_points = [
                "This approach maintains your asking price for appraisal and neighborhood comp purposes",
                "It allows me to address the property issues directly after closing",
                "This can be a tax advantage for both of us compared to a price reduction"
            ]
            
            closing = "This structure gives you the sale price you want while acknowledging the property's condition and necessary improvements."
            
        elif 'As-Is Purchase' in strategy_name:
            discount = strategy.get('discount_needed', 0)
            
            opening = "I'm prepared to purchase the property as-is, without requesting any repairs, but would need to account for the condition in my offer price."
            
            key_points = [
                "I'll conduct an inspection for information only, not for negotiation",
                "This eliminates the risk of repair negotiations or surprises later",
                f"My offer would need to be adjusted by approximately ${discount:,} to account for the needed repairs",
                "This creates a clean, simple transaction with no contingencies for property condition"
            ]
            
            closing = "This approach gives you certainty that the deal won't fall through due to property condition issues, while allowing me to address the needed repairs after closing."
            
        elif 'Seller Pain Point' in strategy_name:
            opening = "I'd like to understand if there are any specific challenges or concerns you have about selling this property, beyond just the price."
            
            solutions = strategy.get('potential_solutions', [])
            key_points = [f"If {solution['pain_point'].lower()} is a concern, I could {solution['solution'].lower()}" for solution in solutions]
            
            closing = "By addressing these specific concerns, we can create a transaction that truly works for your situation, not just a standard deal focused only on price."
            
        elif 'Seller Financing' in strategy_name:
            structure = strategy.get('structure', {})
            
            opening = "I'd like to propose a creative financing structure that might benefit both of us, involving some seller financing."
            
            key_points = [
                f"I would make a ${structure.get('down_payment', 0):,} down payment (20%)",
                f"Get bank financing for ${structure.get('bank_financing', 0):,} (60%)",
                f"And ask you to carry a note for ${structure.get('seller_financing', 0):,} (20%)",
                f"The seller note would be at {structure.get('seller_note_terms', '6% interest')}",
                f"This would provide you with monthly income of approximately ${structure.get('monthly_payment_to_seller', 0):,}"
            ]
            
            closing = "This structure provides you with some immediate cash at closing, plus an ongoing income stream at an interest rate higher than most savings accounts or CDs."
            
        else:
            # Generic creative strategy script
            opening = "I'd like to propose a creative approach to this transaction that might address both our needs better than a standard offer."
            
            key_points = [
                "I've thought about ways to structure this deal that go beyond just the price",
                "My goal is to find a win-win solution that addresses your specific needs",
                "This approach could provide benefits that a traditional transaction might not"
            ]
            
            closing = "I'm open to discussing this creative approach further and adapting it based on your feedback and specific situation."
        
        return {
            'opening_statement': opening,
            'key_points': key_points,
            'closing_statement': closing
        }
    
    def _identify_fallback_options(self, ranked_strategies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Identifies fallback options if the top strategy is rejected
        
        Args:
            ranked_strategies: List of ranked negotiation strategies
            
        Returns:
            List of fallback options
        """
        fallback_options = []
        
        # Need at least 2 strategies to create fallbacks
        if len(ranked_strategies) < 2:
            return fallback_options
        
        # Get top strategy
        top_strategy = ranked_strategies[0]
        
        # If top strategy is price-based, first fallback should be terms or creative
        if top_strategy['type'] == 'price':
            # Find highest ranked non-price strategy
            for strategy in ranked_strategies[1:]:
                if strategy['type'] != 'price':
                    fallback_options.append({
                        'name': f"Switch to {strategy['name']}",
                        'description': f"If price negotiation fails, pivot to {strategy['description']}",
                        'original_strategy': strategy
                    })
                    break
            
            # Add a price compromise fallback
            if 'offer_price' in top_strategy:
                original_offer = top_strategy['offer_price']
                compromise_offer = int(original_offer * 1.03)  # 3% higher than original offer
                
                fallback_options.append({
                    'name': 'Price Compromise',
                    'description': f"Increase offer to ${compromise_offer:,} (3% higher than original)",
                    'compromise_price': compromise_offer,
                    'original_price': original_offer
                })
        
        # If top strategy is terms-based, fallback to price or different terms
        elif top_strategy['type'] == 'terms':
            # Find highest ranked price strategy
            for strategy in ranked_strategies[1:]:
                if strategy['type'] == 'price':
                    fallback_options.append({
                        'name': f"Switch to {strategy['name']}",
                        'description': f"If terms negotiation fails, pivot to {strategy['description']}",
                        'original_strategy': strategy
                    })
                    break
            
            # Add a terms compromise fallback
            fallback_options.append({
                'name': 'Terms Compromise',
                'description': f"Maintain some key terms but be more flexible on others",
                'compromise_approach': "Identify which terms are most important to seller and focus flexibility there"
            })
        
        # If top strategy is creative, fallback to price or terms
        elif top_strategy['type'] == 'creative':
            # Find highest ranked price strategy
            for strategy in ranked_strategies[1:]:
                if strategy['type'] == 'price':
                    fallback_options.append({
                        'name': f"Switch to {strategy['name']}",
                        'description': f"If creative approach fails, pivot to {strategy['description']}",
                        'original_strategy': strategy
                    })
                    break
            
            # Find highest ranked terms strategy
            for strategy in ranked_strategies[1:]:
                if strategy['type'] == 'terms':
                    fallback_options.append({
                        'name': f"Switch to {strategy['name']}",
                        'description': f"If creative approach fails, pivot to {strategy['description']}",
                        'original_strategy': strategy
                    })
                    break
        
        # Add a general compromise fallback if we don't have enough options
        if len(fallback_options) < 2:
            fallback_options.append({
                'name': 'Hybrid Approach',
                'description': "Combine elements from multiple strategies to create a compromise",
                'approach': "Take the strongest elements from each strategy category (price, terms, creative) to create a balanced offer"
            })
        
        return fallback_options
    
    def _calculate_success_probability(self, 
                                      discount_pct: float, 
                                      motivation_level: str, 
                                      market_type: str) -> float:
        """
        Calculates probability of success for a given discount percentage
        
        Args:
            discount_pct: Discount percentage from listing price
            motivation_level: Seller motivation level (high, moderate, low)
            market_type: Market type (buyer, balanced, seller)
            
        Returns:
            Float representing probability of success (0-1)
        """
        # Base probability based on discount percentage
        if discount_pct <= 0.03:
            base_probability = 0.9
        elif discount_pct <= 0.05:
            base_probability = 0.8
        elif discount_pct <= 0.08:
            base_probability = 0.7
        elif discount_pct <= 0.1:
            base_probability = 0.6
        elif discount_pct <= 0.15:
            base_probability = 0.4
        else:
            base_probability = 0.3
        
        # Adjust based on seller motivation
        motivation_factor = 1.0
        if motivation_level == 'high':
            motivation_factor = 1.3
        elif motivation_level == 'moderate':
            motivation_factor = 1.0
        else:  # low
            motivation_factor = 0.7
        
        # Adjust based on market type
        market_factor = 1.0
        if market_type == 'buyer':
            market_factor = 1.2
        elif market_type == 'balanced':
            market_factor = 1.0
        else:  # seller
            market_factor = 0.8
        
        # Calculate final probability
        probability = base_probability * motivation_factor * market_factor
        
        # Cap between 0.1 and 0.95
        return max(0.1, min(0.95, probability))


class NegotiationStrategist:
    """
    Main class for generating negotiation strategies and scripts
    """
    
    def __init__(self):
        """Initialize the NegotiationStrategist"""
        self.strategy_generator = StrategyGenerator()
        
    def generate_strategies(self, 
                           property_data: Dict[str, Any], 
                           market_data: Dict[str, Any], 
                           valuation_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates negotiation strategies based on property, market, and valuation data
        
        Args:
            property_data: Property details and characteristics
            market_data: Market analysis and conditions
            valuation_data: Property valuation and investment analysis
            
        Returns:
            Dict containing negotiation strategies and recommendations
        """
        return self.strategy_generator.generate_strategies(property_data, market_data, valuation_data)


# Example usage
if __name__ == "__main__":
    # Load sample data
    try:
        with open('sample_data.json', 'r') as f:
            sample_data = json.load(f)
            
        property_data = sample_data.get('property', {})
        market_data = sample_data.get('market', {})
        valuation_data = sample_data.get('valuation', {})
        
        # Initialize negotiation strategist
        strategist = NegotiationStrategist()
        
        # Generate negotiation strategies
        negotiation_data = strategist.generate_strategies(property_data, market_data, valuation_data)
        
        # Print results
        print(f"Analysis for {property_data.get('address', 'property')}:")
        print(f"Seller Motivation: {negotiation_data['seller_motivation']['level']} ({negotiation_data['seller_motivation']['score']})")
        print(f"Buyer Leverage: {negotiation_data['buyer_leverage']['level']} ({negotiation_data['buyer_leverage']['score']})")
        
        print("\nTop 3 Recommended Strategies:")
        for i, strategy in enumerate(negotiation_data['recommended_strategies'][:3]):
            print(f"{i+1}. {strategy['name']} - {strategy['description']}")
        
        # Save results to file
        with open('negotiation_strategy_results.json', 'w') as f:
            json.dump(negotiation_data, f, indent=2)
            
        print("\nResults saved to negotiation_strategy_results.json")
        
    except Exception as e:
        print(f"Error generating negotiation strategies: {str(e)}")
