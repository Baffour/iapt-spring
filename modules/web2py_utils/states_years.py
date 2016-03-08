#
#  Copyright (C) 2009 Thadeus Burgess
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>
#


from datetime import datetime

STATES = {
     "AL": "Alabama"
    ,"AK": "Alaska"
    ,"AZ": "Arizona"
    ,"AR": "Arkansas"
    ,"CA": "California"
    ,"CO": "Colorado"
    ,"CT": "Connecticut"
    ,"DE": "Delaware"
    ,"DC": "District of Columbia"
    ,"FL": "Florida"
    ,"GA": "Georgia"
    ,"HI": "Hawaii"
    ,"ID": "Idaho"
    ,"IL": "Illinois"
    ,"IN": "Indiana"
    ,"IA": "Iowa"
    ,"KS": "Kansas"
    ,"KY": "Kentucky"
    ,"LA": "Louisiana"
    ,"ME": "Maine"
    ,"MD": "Maryland"
    ,"MA": "Massachusetts"
    ,"MI": "Michigan"
    ,"MN": "Minnesota"
    ,"MS": "Mississippi"
    ,"MO": "Missouri"
    ,"MT": "Montana"
    ,"NE": "Nebraska"
    ,"NV": "Nevada"
    ,"NH": "New Hampshire"
    ,"NJ": "New Jersey"
    ,"NM": "New Mexico"
    ,"NY": "New York"
    ,"NC": "North Carolina"
    ,"ND": "North Dakota"
    ,"OH": "Ohio"
    ,"OK": "Oklahoma"
    ,"OR": "Oregon"
    ,"PA": "Pennsylvania"
    ,"RI": "Rhode Island"
    ,"SC": "South Carolina"
    ,"SD": "South Dakota"
    ,"TN": "Tennessee"
    ,"TX": "Texas"
    ,"UT": "Utah"
    ,"VT": "Vermont"
    ,"VA": "Virginia"
    ,"WA": "Washington"
    ,"WV": "West Virginia"
    ,"WI": "Wisconsin"
    ,"WY": "Wyoming"
}

STATES_REV = {
    "Alabama":                  "AL",
    "Alaska":                   "AK",
    "Arizona":                  "AZ",
    "Arkansas":                 "AR",
    "California":               "CA",
    "Colorado":                 "CO",
    "Connecticut":              "CT",
    "Delaware":                 "DE",
    "District of Columbia":     "DC",
    "Florida":                  "FL",
    "Georgia":                  "GA",
    "Hawaii":                   "HI",
    "Idaho":                    "ID",
    "Illinois":                 "IL",
    "Indiana":                  "IN",
    "Iowa":                     "IA",
    "Kansas":                   "KS",
    "Kentucky":                 "KY",
    "Louisiana":                "LA",
    "Maine":                    "ME",
    "Maryland":                 "MD",
    "Massachusetts":            "MA",
    "Michigan":                 "MI",
    "Minnesota":                "MN",
    "Mississippi":              "MS",
    "Missouri":                 "MO",
    "Montana":                  "MT",
    "Nebraska":                 "NE",
    "Nevada":                   "NV",
    "New Hampshire":            "NH",
    "New Jersey":               "NJ",
    "New Mexico":               "NM",
    "New York":                 "NY",
    "North Carolina":           "NC",
    "North Dakota":             "ND",
    "Ohio":                     "OH",
    "Oklahoma":                 "OK",
    "Oregon":                   "OR",
    "Pennsylvania":             "PA",
    "Rhode Island":             "RI",
    "South Carolina":           "SC",
    "South Dakota":             "SD",
    "Tennessee":                "TN",
    "Texas":                    "TX",
    "Utah":                     "UT",
    "Vermont":                  "VT",
    "Virginia":                 "VA",
    "Washington":               "WA",
    "West Virginia":            "WV",
    "Wisconsin":                "WI",
    "Wyoming":                  "WY",
}

def states_full():
    STATES_FULL = STATES_REV.keys()
    STATES_FULL.sort()

    return STATES_FULL

def states_abbr():
    # Since you can't sort on the state abbreviation, we
    # need to use the full state name to sort by.

    STATES_ABBR = []

    for f in states_full():
        STATES_ABBR.append(STATES_REV[f])
        
    return STATES_ABBR

def year_list():
    YEAR_LIST = []

    for i in range(1900, datetime.now().year - 17):
        YEAR_LIST.append(i)

    YEAR_LIST.reverse()

    return YEAR_LIST
