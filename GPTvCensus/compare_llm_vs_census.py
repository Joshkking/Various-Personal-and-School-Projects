# %%
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colorbar import ColorbarBase
from matplotlib.ticker import PercentFormatter
import seaborn as sb
sb.set()
import pygris
from pygris.data import get_census


# %%
# Let's first grab a mapping of state abbreviations to state geoids
# and additionally filter down a list to the 50 states (census otherwise includes territories/dc)
l_state_abbreviations = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"
]
df_states = pd.read_csv(
    'https://www2.census.gov/geo/docs/reference/state.txt'
    , sep='|'
    , dtype=str
)
df_states = df_states.query('STUSAB in @l_state_abbreviations')
l_state_geoids = df_states.STATE.to_list()
df_states.head()


# %%
# Grab a dataset of our relevant census variables using pygris
df_census = get_census(
    dataset = 'acs/acs5'
    , variables = [
        'B19013_001E' # Median household income (inflation adjusted 2021 dollars)
        , 'B01003_001E' # Total population
        , 'B01002_001E' # Median Age
        ]
    , params = {'for': 'state:*'}
    , return_geoid = True 
    , year = 2021
    , guess_dtypes = True
    )
df_census.rename(columns={
    'B19013_001E': 'MedHHIncome_Census'
    , 'B01003_001E': 'TotalPop_Census'
    , 'B01002_001E': 'MedAge_Census'
    }
    , inplace=True
    )
df_census.head()


# %%
# Grab our state geographies from TIGER using pygris, filter to the 50 states
dfg_states = pygris.states(year=2021)
dfg_states = dfg_states.query('STATEFP in @l_state_geoids').reset_index(drop=True)
# Let's also add a little better projection and some representative points
dfg_states = dfg_states.to_crs('EPSG:4326')
dfg_states['coords'] = dfg_states['geometry'].apply(lambda x: x.representative_point().coords[0])
dfg_states.head()


# %%
# Merge the shape data and census data together
dfg_states = dfg_states.merge(df_census, on='GEOID', how='inner').reset_index(drop=True)
dfg_states.head()


# %%
# Below is basically just copy pasting gpt's guesses at the census values and assembling into a df
median_incomes_2021_approx = {
    "AL": 50000,
    "AK": 76000,
    "AZ": 59000,
    "AR": 48000,
    "CA": 75000,
    "CO": 70000,
    "CT": 78000,
    "DE": 65000,
    "FL": 58000,
    "GA": 59000,
    "HI": 80000,
    "ID": 58000,
    "IL": 65000,
    "IN": 56000,
    "IA": 60000,
    "KS": 59000,
    "KY": 51000,
    "LA": 49000,
    "ME": 58000,
    "MD": 84000,
    "MA": 81000,
    "MI": 58000,
    "MN": 71000,
    "MS": 44000,
    "MO": 55000,
    "MT": 57000,
    "NE": 61000,
    "NV": 60000,
    "NH": 76000,
    "NJ": 82000,
    "NM": 50000,
    "NY": 70000,
    "NC": 56000,
    "ND": 65000,
    "OH": 58000,
    "OK": 53000,
    "OR": 67000,
    "PA": 63000,
    "RI": 65000,
    "SC": 55000,
    "SD": 58000,
    "TN": 55000,
    "TX": 62000,
    "UT": 70000,
    "VT": 63000,
    "VA": 75000,
    "WA": 74000,
    "WV": 48000,
    "WI": 62000,
    "WY": 65000,
    }
# GPT also wanted to include this inflation adjustment, so I'm running that for it
inflation_adjustment_factor = 1.05
median_incomes_2021 = {
    state: int(income * inflation_adjustment_factor)
    for state, income in median_incomes_2021_approx.items()
    }

df_gpt_income = pd.DataFrame(median_incomes_2021.items(), columns=['STUSAB', 'MedHHIncome_GPT'])
df_gpt = df_gpt_income.merge(df_states.rename(columns={'STATE':'GEOID'}), on='STUSAB')
df_gpt.head()


# %%
median_ages_2021 = {
    'AL': 39.5,  # Alabama
    'AK': 34.6,  # Alaska
    'AZ': 38.2,  # Arizona
    'AR': 38.4,  # Arkansas
    'CA': 36.8,  # California
    'CO': 37.2,  # Colorado
    'CT': 41.2,  # Connecticut
    'DE': 40.7,  # Delaware
    'FL': 42.5,  # Florida
    'GA': 37.4,  # Georgia
    'HI': 39.2,  # Hawaii
    'ID': 36.9,  # Idaho
    'IL': 38.5,  # Illinois
    'IN': 37.9,  # Indiana
    'IA': 38.2,  # Iowa
    'KS': 36.9,  # Kansas
    'KY': 38.9,  # Kentucky
    'LA': 37.1,  # Louisiana
    'ME': 45.1,  # Maine
    'MD': 39.0,  # Maryland
    'MA': 39.5,  # Massachusetts
    'MI': 39.7,  # Michigan
    'MN': 38.0,  # Minnesota
    'MS': 37.8,  # Mississippi
    'MO': 38.6,  # Missouri
    'MT': 39.9,  # Montana
    'NE': 36.8,  # Nebraska
    'NV': 38.1,  # Nevada
    'NH': 43.0,  # New Hampshire
    'NJ': 40.0,  # New Jersey
    'NM': 38.3,  # New Mexico
    'NY': 39.2,  # New York
    'NC': 38.8,  # North Carolina
    'ND': 35.3,  # North Dakota
    'OH': 39.4,  # Ohio
    'OK': 37.0,  # Oklahoma
    'OR': 39.3,  # Oregon
    'PA': 40.8,  # Pennsylvania
    'RI': 40.2,  # Rhode Island
    'SC': 39.5,  # South Carolina
    'SD': 37.1,  # South Dakota
    'TN': 39.0,  # Tennessee
    'TX': 34.8,  # Texas
    'UT': 31.0,  # Utah
    'VT': 43.8,  # Vermont
    'VA': 38.5,  # Virginia
    'WA': 37.9,  # Washington
    'WV': 42.9,  # West Virginia
    'WI': 39.6,  # Wisconsin
    'WY': 38.7   # Wyoming
    }

df_gpt_age = pd.DataFrame(median_ages_2021.items(), columns=['STUSAB', 'MedAge_GPT'])
df_gpt = df_gpt.merge(df_gpt_age.rename(columns={'STATE':'GEOID'}), on='STUSAB')
df_gpt.head()


# %%
us_population_2021 = {
    'AL': 4900000,  # Alabama
    'AK': 730000,   # Alaska
    'AZ': 7500000,  # Arizona
    'AR': 3000000,  # Arkansas
    'CA': 39500000, # California
    'CO': 5800000,  # Colorado
    'CT': 3600000,  # Connecticut
    'DE': 990000,   # Delaware
    'FL': 22000000, # Florida
    'GA': 10500000, # Georgia
    'HI': 1400000,  # Hawaii
    'ID': 1900000,  # Idaho
    'IL': 12600000, # Illinois
    'IN': 6700000,  # Indiana
    'IA': 3150000,  # Iowa
    'KS': 2900000,  # Kansas
    'KY': 4500000,  # Kentucky
    'LA': 4600000,  # Louisiana
    'ME': 1350000,  # Maine
    'MD': 6050000,  # Maryland
    'MA': 6900000,  # Massachusetts
    'MI': 10000000, # Michigan
    'MN': 5650000,  # Minnesota
    'MS': 2900000,  # Mississippi
    'MO': 6150000,  # Missouri
    'MT': 1100000,  # Montana
    'NE': 1950000,  # Nebraska
    'NV': 3100000,  # Nevada
    'NH': 1360000,  # New Hampshire
    'NJ': 9000000,  # New Jersey
    'NM': 2100000,  # New Mexico
    'NY': 19300000, # New York
    'NC': 10500000, # North Carolina
    'ND': 770000,   # North Dakota
    'OH': 11700000, # Ohio
    'OK': 4000000,  # Oklahoma
    'OR': 4200000,  # Oregon
    'PA': 12800000, # Pennsylvania
    'RI': 1050000,  # Rhode Island
    'SC': 5200000,  # South Carolina
    'SD': 890000,   # South Dakota
    'TN': 6900000,  # Tennessee
    'TX': 29000000, # Texas
    'UT': 3300000,  # Utah
    'VT': 630000,   # Vermont
    'VA': 8500000,  # Virginia
    'WA': 7600000,  # Washington
    'WV': 1800000,  # West Virginia
    'WI': 5800000,  # Wisconsin
    'WY': 580000    # Wyoming
    }

df_gpt_pop = pd.DataFrame(us_population_2021.items(), columns=['STUSAB', 'TotalPop_GPT'])
df_gpt = df_gpt.merge(df_gpt_pop.rename(columns={'STATE':'GEOID'}), on='STUSAB')
df_gpt.head()


# %%
# Now join it all together and grab the percent diffs
l_cols_gpt = ['GEOID', 'MedHHIncome_GPT', 'MedAge_GPT', 'TotalPop_GPT']
dfg_states = dfg_states.merge(df_gpt[l_cols_gpt], on='GEOID')
dfg_states['MedHHIncome_PtDiff'] = (100 * (dfg_states.MedHHIncome_GPT - dfg_states.MedHHIncome_Census) / dfg_states.MedHHIncome_Census).round(2)
dfg_states['MedAge_PtDiff'] = (100 * (dfg_states.MedAge_GPT - dfg_states.MedAge_Census) / dfg_states.MedAge_Census).round(2)
dfg_states['TotalPop_PtDiff'] = (100 * (dfg_states.TotalPop_GPT - dfg_states.TotalPop_Census) / dfg_states.TotalPop_Census).round(2)
dfg_states.head()


# %%
# Run some sanity check histograms to get the rough ranges of the errors
dfg_states['MedHHIncome_PtDiff'].hist()

# %%
dfg_states['MedAge_PtDiff'].hist()

# %%
dfg_states['TotalPop_PtDiff'].hist()


# %%
# Wrap all the icky plotting needs together in one function
# Parameterize the colorscale min and max so we can keep this all on the same scale
def plot_var(var_colname, var_displayname, cbar_min=-10, cbar_max=10):

    fig, ax = plt.subplots(figsize=(20,20))

    # Let's do some initial handling to separate alaska and hawaii
    alaska_ax = ax.inset_axes([.08, .01, .20, .28])
    hawaii_ax = ax.inset_axes([.28, .01, .15, .19])
    ax.set_xlim(-130, -64)
    ax.set_ylim(22, 53)
    alaska_ax.set_ylim(51, 72)
    alaska_ax.set_xlim(-180, -127)
    hawaii_ax.set_ylim(18.8, 22.5)
    hawaii_ax.set_xlim(-160, -154.6)

    # Standardize a color bar and norm since alaska and hawaii are plotted separately
    cmap = plt.cm.RdBu
    norm = mcolors.Normalize(
        vmin=cbar_min # dfg_states[var_colname].min()
        , vmax=cbar_max # dfg_states[var_colname].max()
        )

    # Make the basic plots
    dfg_states.plot(ax=ax, column=var_colname, linewidth=0.5, edgecolor='black', cmap=cmap, norm=norm)
    dfg_states.query('NAME == "Alaska"')\
        .plot(ax=alaska_ax, column=var_colname, linewidth=0.5, edgecolor='black', cmap=cmap, norm=norm)
    dfg_states.query('NAME == "Hawaii"')\
        .plot(ax=hawaii_ax, column=var_colname, linewidth=0.5, edgecolor='black', cmap=cmap, norm=norm)

    # Annotate each state but turn off the axis on the bottom and left
    # Annotation offset for specific states
    state_offsets = {
        'Delaware': (0.05, 0),
        'Maryland': (0.05, 0),
        'Rhode Island': (0.05, 0),
        # Add other states here if needed
    }
    # Annotation for each state
    for idx, row in dfg_states.iterrows():
        offset = state_offsets.get(row['NAME'], (0, 0))
        if row['NAME'] == "Alaska":
            current_ax = alaska_ax
        elif row['NAME'] == "Hawaii":
            current_ax = hawaii_ax
        else:
            current_ax = ax
        current_ax.annotate(text='{:.2%}'.format(row[var_colname] / 100.0), xy=(row['coords'][0] + offset[0], row['coords'][1] + offset[1]), ha='center')
    # Turning off the main axis
    for ax in [ax, alaska_ax, hawaii_ax]:
        ax.set_yticks([])
        ax.set_xticks([])

    # Add in a color bar to the right and format it
    cax = fig.add_axes([0.92, 0.3, 0.02, 0.4]) 
    cb = ColorbarBase(cax, cmap=cmap, norm=norm, orientation='vertical')
    cb.ax.yaxis.set_major_formatter(PercentFormatter(100))
    cb.set_label('Percent Error')


    fig.suptitle(f'ChatGPT vs Census \n {var_displayname} Percent Error', fontsize=18, y=0.75)

    plt.savefig(f'{var_colname}.png', bbox_inches='tight')
    plt.show()


# %%
# And run it!
plot_var('MedAge_PtDiff', 'Median Age')
plot_var('MedHHIncome_PtDiff', 'Median Household Income')
plot_var('TotalPop_PtDiff', 'Total Population')


# %%
