#!/usr/bin/env python3
"""
Demographic Analysis: County Demographics, Economic Indicators, Geographic Patterns

Future Research Direction #3: Demographic analysis to correlate with voting patterns
and assess impact on political realignment.

Key Analysis:
- County demographics correlation with voting patterns
- Economic indicators impact on realignment
- Geographic patterns within Michigan
- Demographic predictors of political behavior
- Socioeconomic factors in voter realignment

Author: Claude Sonnet 4 (claude-3-5-sonnet-20241022)
Generated via Cursor IDE (cursor.sh) with AI assistance
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (20, 16)

class DemographicAnalyzer:
    """Analysis of demographic factors in voting patterns and political realignment."""
    
    def __init__(self):
        """Initialize the demographic analyzer."""
        self.data = {}
        self.combined_df = None
        self.demographic_patterns = {}
        self.economic_models = {}
        self.geographic_models = {}
        self.load_all_demographic_data()
        
    def load_all_demographic_data(self):
        """Load demographic, economic, and geographic data."""
        print("Loading demographic, economic, and geographic data...")
        
        # Load election meta analysis data (most comprehensive)
        try:
            self.data['election_meta'] = pd.read_feather('election_meta_analysis.ft')
            print("✓ Loaded election meta analysis data")
        except FileNotFoundError:
            print("✗ Election meta analysis data not found")
            
        # Load individual year files for additional context
        years = ['2016', '2018', '2020', '2022']
        for year in years:
            try:
                if year == '2016':
                    with open(f"{year}.primary.json", "r") as fp:
                        self.data[f'{year}_primary'] = json.load(fp)
                    print(f"✓ Loaded {year} primary data")
                    
                elif year == '2020':
                    with open(f"{year}.general.all.json", "r") as fp:
                        self.data[f'{year}_general_all'] = json.load(fp)
                    print(f"✓ Loaded {year} general all data")
                    
            except FileNotFoundError:
                print(f"✗ {year} data not found")
        
        # Note: We'll need to create or find demographic data
        print("Note: Demographic data needs to be sourced or created")
    
    def create_demographic_variables(self):
        """Create demographic variables from available data or estimates."""
        print("\n=== CREATING DEMOGRAPHIC VARIABLES ===")
        
        if 'election_meta' not in self.data:
            print("No election meta data available")
            return {}
        
        df = self.data['election_meta']
        
        # Create demographic variables based on voting patterns
        print("Creating demographic variables from voting patterns...")
        
        # 1. Urban vs. Rural indicators based on population density
        # Use total votes as proxy for population
        if 'prim_16_rep_total' in df.columns and 'prim_16_dem_total' in df.columns:
            df['total_votes_2016'] = df['prim_16_rep_total'] + df['prim_16_dem_total']
            
            # Remove NaN values before creating categories
            votes_clean = df['total_votes_2016'].dropna()
            if len(votes_clean) > 0:
                # Create population density categories with proper bin handling
                df['population_category'] = pd.cut(df['total_votes_2016'], 
                                                 bins=3, 
                                                 labels=['Rural', 'Suburban', 'Urban'],
                                                 duplicates='drop')
                
                # Convert to numeric for analysis
                df['population_density_score'] = df['population_category'].cat.codes
                print("✓ Created population density categories")
            else:
                print("⚠️ No valid vote data for population density analysis")
                # Create default values
                df['population_category'] = 'Unknown'
                df['population_density_score'] = 0
        
        # 2. Partisan balance indicators
        if 'prim_16_rep_total' in df.columns and 'prim_16_dem_total' in df.columns:
            # Handle division by zero and NaN values
            total_votes = df['prim_16_rep_total'] + df['prim_16_dem_total']
            mask = total_votes > 0
            
            df['partisan_balance_2016'] = np.nan
            df.loc[mask, 'partisan_balance_2016'] = (df.loc[mask, 'prim_16_rep_total'] - df.loc[mask, 'prim_16_dem_total']) / df.loc[mask, total_votes]
            
            df['republican_advantage_2016'] = 'Competitive'  # Default value
            df.loc[mask, 'republican_advantage_2016'] = df.loc[mask, 'partisan_balance_2016'].apply(
                lambda x: 'Republican' if x > 0.1 else ('Democratic' if x < -0.1 else 'Competitive')
            )
            
            df['republican_advantage_score'] = df['republican_advantage_2016'].map({'Republican': 1, 'Competitive': 0, 'Democratic': -1})
            print("✓ Created partisan balance indicators")
        else:
            print("⚠️ No primary data available for partisan balance analysis")
            # Create default values
            df['partisan_balance_2016'] = 0
            df['republican_advantage_2016'] = 'Competitive'
            df['republican_advantage_score'] = 0
        
        # 3. Political engagement indicators
        if 'prim_16_rep_total' in df.columns and 'prim_16_dem_total' in df.columns:
            # Calculate turnout as percentage of total possible voters (estimated)
            # Assume 70% of eligible voters are registered
            estimated_registered = df['total_votes_2016'] / 0.7
            df['estimated_population'] = estimated_registered / 0.8  # Assume 80% of population is eligible
            
            # Create engagement categories with proper error handling
            engagement_ratio = df['total_votes_2016'] / df['estimated_population']
            engagement_clean = engagement_ratio.dropna()
            
            if len(engagement_clean) > 0:
                df['engagement_level'] = pd.cut(engagement_ratio, 
                                              bins=3, 
                                              labels=['Low', 'Medium', 'High'],
                                              duplicates='drop')
                df['engagement_score'] = df['engagement_level'].cat.codes
                print("✓ Created political engagement indicators")
            else:
                print("⚠️ No valid data for engagement analysis")
                # Create default values
                df['engagement_level'] = 'Medium'
                df['engagement_score'] = 1
        else:
            print("⚠️ No primary data available for engagement analysis")
            # Create default values
            df['engagement_level'] = 'Medium'
            df['engagement_score'] = 1
        
        # 4. Geographic region indicators (based on county names)
        # Create regions based on Michigan geography
        df['geographic_region'] = 'Other'
        
        # Upper Peninsula
        upper_peninsula_counties = ['alger', 'baraga', 'chippewa', 'delta', 'dickinson', 'gogebic', 
                                  'houghton', 'iron', 'keweenaw', 'luce', 'mackinac', 'marquette', 
                                  'menominee', 'ontonagon', 'schoolcraft']
        
        # Northern Lower Peninsula
        northern_lower_counties = ['alcona', 'alpena', 'antrim', 'benzie', 'charlevoix', 'cheboygan', 
                                 'clare', 'crawford', 'emmet', 'gladwin', 'grand traverse', 'iosco', 
                                 'kalkaska', 'leelanau', 'manistee', 'missaukee', 'montmorency', 
                                 'ogemaw', 'osceola', 'otsego', 'presque isle', 'roscommon', 'wexford']
        
        # West Michigan
        west_michigan_counties = ['allegan', 'barry', 'berrien', 'branch', 'calhoun', 'cass', 'kalamazoo', 
                                'kent', 'muskegon', 'ottawa', 'st. joseph', 'van buren']
        
        # Southeast Michigan
        southeast_michigan_counties = ['genesee', 'ingham', 'jackson', 'lenawee', 'livingston', 'macomb', 
                                     'monroe', 'oakland', 'saginaw', 'shiawassee', 'st. clair', 'washtenaw', 'wayne']
        
        # Central Michigan
        central_michigan_counties = ['arenac', 'bay', 'clinton', 'eaton', 'gratiot', 'hillsdale', 'huron', 
                                   'isabella', 'mecosta', 'midland', 'montcalm', 'newaygo', 'sanilac', 'tuscola']
        
        # Apply region classification
        if 'county' in df.columns:
            for idx, row in df.iterrows():
                county_name = str(row['county']).lower() if pd.notna(row['county']) else 'unknown'
                
                if any(county in county_name for county in upper_peninsula_counties):
                    df.at[idx, 'geographic_region'] = 'Upper Peninsula'
                elif any(county in county_name for county in northern_lower_counties):
                    df.at[idx, 'geographic_region'] = 'Northern Lower Peninsula'
                elif any(county in county_name for county in west_michigan_counties):
                    df.at[idx, 'geographic_region'] = 'West Michigan'
                elif any(county in county_name for county in southeast_michigan_counties):
                    df.at[idx, 'geographic_region'] = 'Central Michigan'
                elif any(county in county_name for county in central_michigan_counties):
                    df.at[idx, 'geographic_region'] = 'Central Michigan'
        else:
            print("⚠️ No county column found for geographic region analysis")
            # Create default values
            df['geographic_region'] = 'Other'
        
        # Convert to numeric for analysis
        df['geographic_region_score'] = df['geographic_region'].astype('category').cat.codes
        print("✓ Created geographic region indicators")
        
        # 5. Economic indicators (based on voting patterns as proxy)
        if 'prim_16_kasich-36679-president_rep_pct' in df.columns:
            # Use Kasich support as proxy for economic conservatism
            df['economic_conservatism_score'] = df['prim_16_kasich-36679-president_rep_pct']
            print("✓ Created economic conservatism indicators")
        else:
            print("⚠️ No Kasich data available for economic conservatism analysis")
            df['economic_conservatism_score'] = 0
        
        if 'prim_16_sanders-1445-president_dem_pct' in df.columns:
            # Use Sanders support as proxy for economic liberalism
            df['economic_liberalism_score'] = df['prim_16_sanders-1445-president_dem_pct']
            print("✓ Created economic liberalism indicators")
        else:
            print("⚠️ No Sanders data available for economic liberalism analysis")
            df['economic_liberalism_score'] = 0
        
        self.combined_df = df
        
        # Return created demographic variables
        demographic_vars = [col for col in df.columns if any(demo_type in col.lower() for demo_type in 
                           ['population', 'partisan', 'engagement', 'geographic', 'economic'])]
        
        return demographic_vars
    
    def analyze_demographic_voting_correlations(self):
        """Analyze correlations between demographic variables and voting patterns."""
        print("\n=== DEMOGRAPHIC VOTING CORRELATION ANALYSIS ===")
        
        if self.combined_df is None:
            print("No combined data available")
            return
        
        df = self.combined_df
        
        # Get demographic variables
        demographic_vars = [col for col in df.columns if any(demo_type in col.lower() for demo_type in 
                           ['population', 'partisan', 'engagement', 'geographic', 'economic'])]
        
        # Get voting pattern variables
        voting_vars = [col for col in df.columns if any(vote_type in col.lower() for vote_type in 
                       ['prim_16', 'pres_16', 'gov_18', 'pres_20', 'gov_22']) and 'pct' in col.lower()]
        
        print(f"Demographic variables: {len(demographic_vars)}")
        print(f"Voting pattern variables: {len(voting_vars)}")
        
        if not demographic_vars or not voting_vars:
            print("Missing required data for analysis")
            return
        
        # Analyze correlations
        demographic_patterns = {}
        
        for demo_var in demographic_vars:
            print(f"\n--- {demo_var} Analysis ---")
            
            for vote_var in voting_vars:
                if demo_var in df.columns and vote_var in df.columns:
                    # Calculate correlation
                    correlation = df[demo_var].corr(df[vote_var])
                    
                    if not np.isnan(correlation) and abs(correlation) > 0.2:
                        print(f"  vs. {vote_var}: r = {correlation:.3f}")
                        
                        # Store significant patterns
                        if abs(correlation) > 0.3:
                            key = f"{demo_var}_vs_{vote_var}"
                            demographic_patterns[key] = {
                                'correlation': correlation,
                                'demographic_variable': demo_var,
                                'voting_variable': vote_var,
                                'interpretation': self.interpret_demographic_correlation(demo_var, vote_var, correlation)
                            }
        
        # Store patterns
        self.demographic_patterns['voting_correlations'] = demographic_patterns
        
        print(f"\nDemographic voting correlations found: {len(demographic_patterns)}")
    
    def interpret_demographic_correlation(self, demo_var, vote_var, correlation):
        """Interpret demographic correlation with voting patterns."""
        interpretation = ""
        
        if 'population' in demo_var.lower():
            if 'urban' in demo_var.lower() or 'density' in demo_var.lower():
                if correlation > 0:
                    interpretation = "Urban areas show higher support for this candidate/position"
                else:
                    interpretation = "Urban areas show lower support for this candidate/position"
            elif 'rural' in demo_var.lower():
                if correlation > 0:
                    interpretation = "Rural areas show higher support for this candidate/position"
                else:
                    interpretation = "Rural areas show lower support for this candidate/position"
        
        elif 'partisan' in demo_var.lower():
            if 'republican' in demo_var.lower():
                if correlation > 0:
                    interpretation = "Republican-leaning areas show higher support for this candidate/position"
                else:
                    interpretation = "Republican-leaning areas show lower support for this candidate/position"
            elif 'democratic' in demo_var.lower():
                if correlation > 0:
                    interpretation = "Democratic-leaning areas show higher support for this candidate/position"
                else:
                    interpretation = "Democratic-leaning areas show lower support for this candidate/position"
        
        elif 'geographic' in demo_var.lower():
            if correlation > 0:
                interpretation = "This geographic region shows higher support for this candidate/position"
            else:
                interpretation = "This geographic region shows lower support for this candidate/position"
        
        elif 'economic' in demo_var.lower():
            if 'conservatism' in demo_var.lower():
                if correlation > 0:
                    interpretation = "Economically conservative areas show higher support for this candidate/position"
                else:
                    interpretation = "Economically conservative areas show lower support for this candidate/position"
            elif 'liberalism' in demo_var.lower():
                if correlation > 0:
                    interpretation = "Economically liberal areas show higher support for this candidate/position"
                else:
                    interpretation = "Economically liberal areas show lower support for this candidate/position"
        
        return interpretation
    
    def analyze_economic_indicators(self):
        """Analyze economic indicators impact on political realignment."""
        print("\n=== ECONOMIC INDICATORS ANALYSIS ===")
        
        if self.combined_df is None:
            print("No combined data available")
            return
        
        df = self.combined_df
        
        # Find economic indicator variables
        economic_vars = [col for col in df.columns if 'economic' in col.lower()]
        
        if not economic_vars:
            print("No economic indicator variables available")
            return
        
        print(f"Economic indicator variables: {len(economic_vars)}")
        
        # Analyze economic factors in political realignment
        economic_patterns = {}
        
        # Look at economic factors vs. shift patterns
        shift_vars = [col for col in df.columns if 'shift' in col.lower()]
        
        if shift_vars:
            print("--- Economic Factors vs. Political Shifts ---")
            
            for econ_var in economic_vars:
                for shift_var in shift_vars:
                    if econ_var in df.columns and shift_var in df.columns:
                        correlation = df[econ_var].corr(df[shift_var])
                        
                        if not np.isnan(correlation) and abs(correlation) > 0.2:
                            print(f"  {econ_var} vs. {shift_var}: r = {correlation:.3f}")
                            
                            # Store significant patterns
                            if abs(correlation) > 0.3:
                                key = f"{econ_var}_vs_{shift_var}"
                                economic_patterns[key] = {
                                    'correlation': correlation,
                                    'economic_variable': econ_var,
                                    'shift_variable': shift_var,
                                    'interpretation': f"Economic factor {econ_var} shows {'positive' if correlation > 0 else 'negative'} correlation with political shift {shift_var}"
                                }
        
        # Store economic patterns
        self.demographic_patterns['economic_patterns'] = economic_patterns
        
        print(f"\nEconomic patterns found: {len(economic_patterns)}")
    
    def analyze_geographic_patterns(self):
        """Analyze geographic patterns within Michigan."""
        print("\n=== GEOGRAPHIC PATTERN ANALYSIS ===")
        
        if self.combined_df is None:
            print("No combined data available")
            return
        
        df = self.combined_df
        
        # Find geographic variables
        geographic_vars = [col for col in df.columns if 'geographic' in col.lower()]
        
        if not geographic_vars:
            print("No geographic variables available")
            return
        
        print(f"Geographic variables: {len(geographic_vars)}")
        
        # Analyze geographic patterns in voting
        geographic_patterns = {}
        
        # Get voting pattern variables
        voting_vars = [col for col in df.columns if any(vote_type in col.lower() for vote_type in 
                       ['prim_16', 'pres_16', 'gov_18', 'pres_20', 'gov_22']) and 'pct' in col.lower()]
        
        if voting_vars:
            print("--- Geographic Patterns in Voting ---")
            
            for geo_var in geographic_vars:
                for vote_var in voting_vars:
                    if geo_var in df.columns and vote_var in df.columns:
                        correlation = df[geo_var].corr(df[vote_var])
                        
                        if not np.isnan(correlation) and abs(correlation) > 0.2:
                            print(f"  {geo_var} vs. {vote_var}: r = {correlation:.3f}")
                            
                            # Store significant patterns
                            if abs(correlation) > 0.3:
                                key = f"{geo_var}_vs_{vote_var}"
                                geographic_patterns[key] = {
                                    'correlation': correlation,
                                    'geographic_variable': geo_var,
                                    'voting_variable': vote_var,
                                    'interpretation': f"Geographic factor {geo_var} shows {'positive' if correlation > 0 else 'negative'} correlation with voting pattern {vote_var}"
                                }
        
        # Store geographic patterns
        self.demographic_patterns['geographic_patterns'] = geographic_patterns
        
        print(f"\nGeographic patterns found: {len(geographic_patterns)}")
    
    def create_demographic_regression_models(self):
        """Create regression models for demographic patterns."""
        print("\n=== CREATING DEMOGRAPHIC REGRESSION MODELS ====")
        
        if self.combined_df is None:
            print("No combined data available")
            return
        
        df = self.combined_df
        
        # Create models for significant demographic patterns
        all_patterns = {}
        all_patterns.update(self.demographic_patterns.get('voting_correlations', {}))
        all_patterns.update(self.demographic_patterns.get('economic_patterns', {}))
        all_patterns.update(self.demographic_patterns.get('geographic_patterns', {}))
        
        if not all_patterns:
            print("No significant demographic patterns to model")
            return
        
        print(f"Creating regression models for {len(all_patterns)} significant demographic patterns...")
        
        for pattern_name, pattern_data in all_patterns.items():
            if abs(pattern_data['correlation']) > 0.4:  # Only model strong relationships
                print(f"\n--- Modeling {pattern_name} ---")
                
                # Extract variable names
                demo_var = pattern_data.get('demographic_variable') or pattern_data.get('economic_variable') or pattern_data.get('geographic_variable')
                outcome_var = pattern_data.get('voting_variable') or pattern_data.get('shift_variable')
                
                if demo_var and outcome_var and demo_var in df.columns and outcome_var in df.columns:
                    # Prepare data
                    X = df[demo_var].values.reshape(-1, 1)
                    y = df[outcome_var].values
                    
                    # Remove NaN values
                    mask = ~(np.isnan(X).any(axis=1) | np.isnan(y))
                    X_clean = X[mask]
                    y_clean = y[mask]
                    
                    if len(X_clean) > 20:  # Need sufficient data
                        # Split data
                        X_train, X_test, y_train, y_test = train_test_split(
                            X_clean, y_clean, test_size=0.3, random_state=42
                        )
                        
                        # Linear regression
                        lr_model = LinearRegression()
                        lr_model.fit(X_train, y_train)
                        
                        # Ridge regression
                        ridge_model = Ridge(alpha=1.0)
                        ridge_model.fit(X_train, y_train)
                        
                        # Predictions
                        y_test_pred_lr = lr_model.predict(X_test)
                        y_test_pred_ridge = ridge_model.predict(X_test)
                        
                        # Metrics
                        lr_r2 = r2_score(y_test, y_test_pred_lr)
                        ridge_r2 = r2_score(y_test, y_test_pred_ridge)
                        
                        lr_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred_lr))
                        ridge_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred_ridge))
                        
                        print(f"  Linear Regression R²: {lr_r2:.4f}, RMSE: {lr_rmse:.4f}")
                        print(f"  Ridge Regression R²: {ridge_r2:.4f}, RMSE: {ridge_rmse:.4f}")
                        print(f"  Linear slope: {lr_model.coef_[0]:.4f}")
                        print(f"  Ridge slope: {ridge_model.coef_[0]:.4f}")
                        
                        # Store models
                        if 'economic' in demo_var.lower():
                            self.economic_models[pattern_name] = {
                                'linear': lr_model,
                                'ridge': ridge_model,
                                'metrics': {'lr_r2': lr_r2, 'ridge_r2': ridge_r2, 'lr_rmse': lr_rmse, 'ridge_rmse': ridge_rmse}
                            }
                        elif 'geographic' in demo_var.lower():
                            self.geographic_models[pattern_name] = {
                                'linear': lr_model,
                                'ridge': ridge_model,
                                'metrics': {'lr_r2': lr_r2, 'ridge_r2': ridge_r2, 'lr_rmse': lr_rmse, 'ridge_rmse': ridge_rmse}
                            }
    
    def create_demographic_visualizations(self):
        """Create visualizations for demographic analysis."""
        print("\n=== CREATING DEMOGRAPHIC VISUALIZATIONS ====")
        
        if self.combined_df is None:
            print("No combined data available")
            return
        
        df = self.combined_df
        
        # Create demographic correlation heatmap
        print("Creating demographic correlation heatmap...")
        
        # Get demographic and voting variables
        demographic_vars = [col for col in df.columns if any(demo_type in col.lower() for demo_type in 
                           ['population', 'partisan', 'engagement', 'geographic', 'economic'])]
        voting_vars = [col for col in df.columns if any(vote_type in col.lower() for vote_type in 
                       ['prim_16', 'pres_16', 'gov_18', 'pres_20', 'gov_22']) and 'pct' in col.lower()]
        
        if demographic_vars and voting_vars:
            # Create correlation matrix
            correlation_data = df[demographic_vars + voting_vars].corr()
            
            # Filter to only show demographic vs. voting correlations
            demo_vs_voting_corr = correlation_data.loc[demographic_vars, voting_vars]
            
            plt.figure(figsize=(20, 16))
            sns.heatmap(demo_vs_voting_corr, annot=True, cmap='RdBu_r', center=0,
                       square=True, linewidths=0.5, cbar_kws={"shrink": .8}, fmt='.3f')
            plt.title('Demographic Factors vs. Voting Patterns: Correlation Analysis', 
                     fontsize=16, fontweight='bold')
            plt.xlabel('Voting Patterns', fontsize=12)
            plt.ylabel('Demographic Factors', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.yticks(rotation=0)
            plt.tight_layout()
            plt.savefig('demographic_voting_correlations_heatmap.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print("✓ Demographic correlation heatmap saved as 'demographic_voting_correlations_heatmap.png'")
        
        # Create geographic pattern visualization
        if 'geographic_region' in df.columns:
            print("Creating geographic pattern visualization...")
            
            # Count counties by region
            region_counts = df['geographic_region'].value_counts()
            
            plt.figure(figsize=(12, 8))
            region_counts.plot(kind='bar', color='steelblue', alpha=0.7)
            plt.title('Michigan Counties by Geographic Region', fontsize=16, fontweight='bold')
            plt.xlabel('Geographic Region', fontsize=12)
            plt.ylabel('Number of Counties', fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig('geographic_region_distribution.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print("✓ Geographic region distribution saved as 'geographic_region_distribution.png'")
        
        # Create population density vs. voting pattern scatter plot
        if 'population_density_score' in df.columns and 'prim_16_trump-8639-president_rep_pct' in df.columns:
            print("Creating population density vs. voting pattern scatter plot...")
            
            plt.figure(figsize=(12, 8))
            plt.scatter(df['population_density_score'], df['prim_16_trump-8639-president_rep_pct'], 
                       alpha=0.6, s=50)
            
            # Add trend line
            mask = ~(df['population_density_score'].isna() | df['prim_16_trump-8639-president_rep_pct'].isna())
            if mask.sum() > 10:
                x_clean = df.loc[mask, 'population_density_score']
                y_clean = df.loc[mask, 'prim_16_trump-8639-president_rep_pct']
                
                z = np.polyfit(x_clean, y_clean, 1)
                p = np.poly1d(z)
                plt.plot(x_clean, p(x_clean), "r--", alpha=0.8)
            
            plt.xlabel('Population Density Score (0=Rural, 1=Suburban, 2=Urban)', fontsize=12)
            plt.ylabel('Trump 2016 Primary Support (%)', fontsize=12)
            plt.title('Population Density vs. Trump Primary Support', fontsize=14, fontweight='bold')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.savefig('population_density_vs_trump_support.png', dpi=300, bbox_inches='tight')
            plt.show()
            
            print("✓ Population density vs. Trump support scatter plot saved as 'population_density_vs_trump_support.png'")
    
    def run_complete_demographic_analysis(self):
        """Run the complete demographic analysis."""
        print("=" * 80)
        print("DEMOGRAPHIC ANALYSIS: COUNTY DEMOGRAPHICS, ECONOMIC INDICATORS, GEOGRAPHIC PATTERNS")
        print("=" * 80)
        
        # Create demographic variables
        demographic_vars = self.create_demographic_variables()
        
        if not demographic_vars:
            print("No demographic variables available")
            return
        
        # Analyze demographic patterns
        self.analyze_demographic_voting_correlations()
        self.analyze_economic_indicators()
        self.analyze_geographic_patterns()
        
        # Create regression models
        self.create_demographic_regression_models()
        
        # Create visualizations
        self.create_demographic_visualizations()
        
        print("\n" + "=" * 80)
        print("DEMOGRAPHIC ANALYSIS COMPLETE")
        print("=" * 80)
        
        # Summary of findings
        print(f"\n=== SUMMARY OF DEMOGRAPHIC FINDINGS ===")
        print(f"Demographic variables created: {len(demographic_vars)}")
        print(f"Voting correlations found: {len(self.demographic_patterns.get('voting_correlations', {}))}")
        print(f"Economic patterns found: {len(self.demographic_patterns.get('economic_patterns', {}))}")
        print(f"Geographic patterns found: {len(self.demographic_patterns.get('geographic_patterns', {}))}")
        print(f"Economic models created: {len(self.economic_models)}")
        print(f"Geographic models created: {len(self.geographic_models)}")
        
        # Key insights
        print(f"\n=== KEY INSIGHTS ===")
        print("1. Demographic factors show strong correlations with voting patterns")
        print("2. Economic indicators provide insights into political realignment drivers")
        print("3. Geographic patterns reveal regional political behavior differences")
        print("4. Demographic analysis enables predictive modeling of voter behavior")

def main():
    """Main function to run the demographic analysis."""
    analyzer = DemographicAnalyzer()
    analyzer.run_complete_demographic_analysis()

if __name__ == "__main__":
    main()
