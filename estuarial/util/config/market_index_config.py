"""
Configuration and constants for MarketIndex.

Author: Ben Zaitlen and Ely Spears


Some raw queries useful for obtaining the info encoded below:

-- S & P
select * 
from idxinfo 
where code in (select distinct idxcode 
               from idxspcmp)

-- Russell
select * 
from idxinfo 
where code in (select distinct idxcode 
               from idxrlcmp)   

-- Dow
select * 
from idxinfo 
where code in (select distinct idxcode 
               from idxdjcmp)   

 -- S&P BMI
select * 
from idxbmiinfo 
where idxcode in (select distinct idxcode 
                  from IdxBMIConst)
"""

# Dictionary that maps the exposed, convenience-function name of an index (as
# the key) to a pair, the function to call within market_index.py to retrieve
# that index's values, and the identifier (ITICKER) needed to identify the 
# index within the query that the function will run.
_SUPPORTED_INDICES = {
    # Dow Jones
    "Dow Jones": ("dowjones_universe", "DJX_IDX"),

    # Russell
    "Russell 1000": ("russell_universe", "RUI_IDX"),
    "Russell 2000": ("russell_universe", "RUT_IDX"),
    "Russell 3000": ("russell_universe", "RUA_IDX"),            

    # S&P US indices
    "S&P 100":  ("spx_universe", "OEX_IDX"),        
    "S&P 500":  ("spx_universe", "SPX_IDX"),
    "S&P 900":  ("spx_universe", "SQUQK_IDX"),
    "S&P 1000": ("spx_universe", "LEB3K_IDX"),

    # S&P BMI indices
    "S&P Greece BMI":                        ("bmi_universe", "SPCBMICGRUSD"),
    "S&P Hong Kong BMI":                     ("bmi_universe", "SPCBMICHKUSD"),
    "S&P Hungary BMI":                       ("bmi_universe", "SPCBMICHUUSD"),
    "S&P Indonesia BMI":                     ("bmi_universe", "SPCBMICIDUSD"),
    "S&P Ireland BMI":                       ("bmi_universe", "SPCBMICIEUSD"),
    "S&P Israel BMI":                        ("bmi_universe", "SPCBMICILUSD"),
    "S&P India BMI":                         ("bmi_universe", "SPCBMICINUSD"),
    "S&P Iceland BMI":                       ("bmi_universe", "SPCBMICISUSD"),
    "S&P Italy BMI":                         ("bmi_universe", "SPCBMICITUSD"),
    "S&P Jordan BMI":                        ("bmi_universe", "SPCBMICJOUSD"),
    "S&P Japan BMI":                         ("bmi_universe", "SPCBMICJPUSD"),
    "S&P Korea BMI":                         ("bmi_universe", "SPCBMICKRUSD"),
    "S&P Luxembourg BMI":                    ("bmi_universe", "SPCBMICLUUSD"),
    "S&P Morocco BMI":                       ("bmi_universe", "SPCBMICMAUSD"),
    "S&P Mexico BMI":                        ("bmi_universe", "SPCBMICMXUSD"),
    "S&P Argentina BMI":                     ("bmi_universe", "SPCBMICARUSD"),
    "S&P Austria BMI":                       ("bmi_universe", "SPCBMICATUSD"),
    "S&P Australia BMI":                     ("bmi_universe", "SPCBMICAUUSD"),
    "S&P Belgium BMI":                       ("bmi_universe", "SPCBMICBEUSD"),
    "S&P Brazil BMI":                        ("bmi_universe", "SPCBMICBRUSD"),
    "S&P Canada BMI":                        ("bmi_universe", "SPCBMICCAUSD"),
    "S&P Switzerland BMI":                   ("bmi_universe", "SPCBMICCHUSD"),
    "S&P Chile BMI":                         ("bmi_universe", "SPCBMICCLUSD"),
    "S&P China BMI":                         ("bmi_universe", "SPCBMICCNUSD"),
    "S&P Colombia BMI":                      ("bmi_universe", "SPCBMICCOUSD"),
    "S&P Czech Republic BMI":                ("bmi_universe", "SPCBMICCZUSD"),
    "S&P Germany BMI":                       ("bmi_universe", "SPCBMICDEUSD"),
    "S&P Denmark BMI":                       ("bmi_universe", "SPCBMICDKUSD"),
    "S&P Egypt BMI":                         ("bmi_universe", "SPCBMICEGUSD"),
    "S&P Spain BMI":                         ("bmi_universe", "SPCBMICESUSD"),
    "S&P Finland BMI":                       ("bmi_universe", "SPCBMICFIUSD"),
    "S&P France BMI":                        ("bmi_universe", "SPCBMICFRUSD"),
    "S&P United Kingdom BMI":                ("bmi_universe", "SPCBMICGBUSD"),
    "S&P EPAC BMI":                          ("bmi_universe", "SPCBMIREPUSD"),
    "S&P Europe Ex-Switzerland BMI":         ("bmi_universe", "SPCBMIRESUSD"),
    "S&P Europe BMI":                        ("bmi_universe", "SPCBMIREUUSD"),
    "S&P Europe Ex-U.K. BMI":                ("bmi_universe", "SPCBMIREXUSD"),
    "S&P Eurozone BMI":                      ("bmi_universe", "SPCBMIREZUSD"),
    "S&P Global Ex-Japan BMI":               ("bmi_universe", "SPCBMIRGJUSD"),
    "S&P Global BMI":                        ("bmi_universe", "SPCBMIRGLUSD"),
    "S&P Global Ex-Pan Asia BMI":            ("bmi_universe", "SPCBMIRGSUSD"),
    "S&P Malaysia BMI":                      ("bmi_universe", "SPCBMICMYUSD"),
    "S&P Nigeria BMI":                       ("bmi_universe", "SPCBMICNGUSD"),
    "S&P Netherlands BMI":                   ("bmi_universe", "SPCBMICNLUSD"),
    "S&P Norway BMI":                        ("bmi_universe", "SPCBMICNOUSD"),
    "S&P New Zealand BMI":                   ("bmi_universe", "SPCBMICNZUSD"),
    "S&P Peru BMI":                          ("bmi_universe", "SPCBMICPEUSD"),
    "S&P Philippines BMI":                   ("bmi_universe", "SPCBMICPHUSD"),
    "S&P Pakistan BMI":                      ("bmi_universe", "SPCBMICPKUSD"),
    "S&P Poland BMI":                        ("bmi_universe", "SPCBMICPLUSD"),
    "S&P Portugal BMI":                      ("bmi_universe", "SPCBMICPTUSD"),
    "S&P Asia Pacific Emerging BMI":         ("bmi_universe", "SPCBMIRAEUSD"),
    "S&P Asia Pacific Ex-Japan BMI":         ("bmi_universe", "SPCBMIRAJUSD"),
    "S&P Americas BMI":                      ("bmi_universe", "SPCBMIRAMUSD"),
    "S&P Global Ex-U.S. BMI":                ("bmi_universe", "SPCBMIRGUUSD"),
    "S&P Developed Ex-U.S. & Japan BMI":     ("bmi_universe", "SPCBMIRIJUSD"),
    "S&P Developed Ex-U.S. & U.K. BMI":      ("bmi_universe", "SPCBMIRIKUSD"),
    "S&P Latin America BMI":                 ("bmi_universe", "SPCBMIRLAUSD"),
    "S&P Emg Europe, Mid-East & Africa BMI": ("bmi_universe", "PCBMIRM1USD",),
    "S&P Mid-East and Africa Emerging BMI":  ("bmi_universe", "PCBMIRMEUSD",),
    "S&P North America BMI":                 ("bmi_universe", "PCBMIRNAUSD",),
    "S&P Europe, Mid-East & Africa BMI":     ("bmi_universe", "PCBMIROWUSD",),
    "S&P Greater China BMI":                 ("bmi_universe", "SPCBMIRP2USD"),
    "S&P Pan Asia BMI":                      ("bmi_universe", "SPCBMIRPAUSD"),
    "S&P Pan Europe BMI":                    ("bmi_universe", "SPCBMIRPEUSD"),
    "S&P Pan Asia Ex-Japan BMI":             ("bmi_universe", "SPCBMIRPJUSD"),
    "S&P Asia Pacific BMI":                  ("bmi_universe", "SPCBMIRAPUSD"),
    "S&P Asia Pacfic Ex-ANZ BMI":            ("bmi_universe", "SPCBMIRAZUSD"),
    "S&P Developed Ex-Eurozone BMI":         ("bmi_universe", "SPCBMIRB3USD"),
    "S&P European Emerging BMI":             ("bmi_universe", "SPCBMIREEUSD"),
    "S&P EPAC Ex-Japan BMI":                 ("bmi_universe", "SPCBMIREJUSD"),
    "S&P Emerging BMI":                      ("bmi_universe", "SPCBMIREMUSD"),
    "S&P Developed Ex-U.K. BMI":             ("bmi_universe", "SPCBMIRWKUSD"),
    "S&P Developed Ex-Asia-Pacific BMI":     ("bmi_universe", "SPCBMIRWPUSD"),
    "S&P Developed Ex-U.S. BMI":             ("bmi_universe", "SPCBMIRWUUSD"),
    "S&P Developed Ex-Switzerland BMI":      ("bmi_universe", "SPCBMIRWZUSD"),
    "S&P AU + NZ BMI":                       ("bmi_universe", "SPCBMIRZAUSD"),
    "S&P Sweden BMI":                        ("bmi_universe", "SPCBMICSEUSD"),
    "S&P Pan Asia Ex-AU Ex-NZ BMI":          ("bmi_universe", "SPCBMIRPUUSD"),
    "S&P Nordic BMI":                        ("bmi_universe", "SPCBMIRSCUSD"),
    "S&P Russian Federation BMI":            ("bmi_universe", "SPCBMICRUUSD"),
    "S&P Developed Ex-Australia BMI":        ("bmi_universe", "SPCBMIRWAUSD"),
    "S&P Developed Ex-Canada BMI":           ("bmi_universe", "SPCBMIRWCUSD"),
    "S&P Developed BMI":                     ("bmi_universe", "SPCBMIRWDUSD"),
    "S&P Developed Ex-Europe BMI":           ("bmi_universe", "SPCBMIRWEUSD"),
    "S&P Developed Ex-Japan BMI":            ("bmi_universe", "SPCBMIRWJUSD"),
    "S&P Singapore BMI":                     ("bmi_universe", "SPCBMICSGUSD"),
    "S&P Slovenia BMI":                      ("bmi_universe", "SPCBMICSIUSD"),
    "S&P Thailand BMI":                      ("bmi_universe", "SPCBMICTHUSD"),
    "S&P Turkey BMI":                        ("bmi_universe", "SPCBMICTRUSD"),
    "S&P Taiwan BMI":                        ("bmi_universe", "SPCBMICTWUSD"),
    "S&P United States BMI":                 ("bmi_universe", "SPCBMICUSUSD"),
    "S&P Venezuela BMI":                     ("bmi_universe", "SPCBMICVEUSD"),
    "S&P South Africa BMI":                  ("bmi_universe", "SPCBMICZAUSD"),
    "S&P Pan Asia Ex-Japan, AU, NZ BMI":     ("bmi_universe", "SPAXANJP"),
    "S&P EPAC Ex-Israel BMI":                ("bmi_universe", "SPCBMIREIUSD"),
    "S&P Mid-East & Africa Developed BMI":   ("bmi_universe", "SPCBMIRMDUSD"),
    "S&P Developed Ex-Israel BMI":           ("bmi_universe", "SPCBMIRWIUSD"),
}
