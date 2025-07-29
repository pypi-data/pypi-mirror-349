# wsa-toetsing-tool
This is the `wsa_toetsing_tool`, a Python package designed to facilitate testing and evaluation processes.

## Installation
You can install the package using pip, but it is dependent on the correct python and GDAL versions.

### Using conda

 Run the following command in your terminal (replace ```<<name>>``` with the name you would like for your environment):

```
conda create --name <<name>> python=3.10
conda activate <<name>>
conda install -c conda-forge gdal==3.6.2
set GDAL_VERSION=3.6.2
pip install wsa_toetsing_tool
```

## Usage

This tool can be used command line. The following commands are available:
- ```bergingstoets```
- ```knelpuntanalyse```
- ```compensatie_scenarios```
- ```compensatie_toetshoogte```
- ```samenvoegen_resultaten```

Type ```<<command>> --help``` for more information regarding the usage.

### Example workflow:
1. Execute bergingstoets: ```bergingstoets --settings "c:/path/to/settings.ini"```
2. **Manually check the outcome and improve 'toetshoogte' before using it in further analysis**
3. Execute knelpuntenanalyse for multiple scenarios:
    * ```knelpuntanalyse --settings " c:/path/to/settings.ini"  --scenario_settings "c:/path/to/scenario_1_settings.ini"```
    * ```knelpuntanalyse --settings " c:/path/to/settings.ini"  --scenario_settings "c:/path/to/scenario_1_settings.ini"``` 
4. Calculate the compansation between 2 scenarios: ```compensatie_scenarios --settings "c:/path/to/settings.ini" --referentiescenario "c:/path/to/scenario_1_settings.ini" --vergelijkscenario "c:/path/to/scenario_2_settings.ini"```
5. Calculate the compensation between a scenario and the 'toetshoogte': ```scenario_toetshoogte -settings "c:/path/to/settings.ini" --scenario_settings "c:/path/to/scenario_1_settings"```
6. Combine results: ```samenvoegen_resultaten --settings "c:/path/to/settings.ini" --reference_scenario_settings "c:/path/to/scenario_1_settings.ini" --scenario_settings "c:/path/to/scenario_2_settings.ini"``` 

### Folder structure
The folder structure should be like below. In a main folder there should be the settings files. All file referals in the settings files are relative to the locations of the settings files.

```bash
.
├── input
│   ├── elevation_model.tif
│   └── some_shapefile.shp
├── settings.ini
├── settings_WH2050.ini
├── settings_WH2085.ini
└── settings_huidig.ini
```

### - settings.ini - 
```
[output]
wsa_titel = BBO                                         # Titel van de WSA
folder_pad = output/bbo                                 # Relatieve pad waar de uitvoer weggeschreven moet worden
prefix = bbo_                                           # Prefix die gebruikt wordt om aan de bestandsnamen toe te voegen

[normen]
bestand_pad = input/BGT/BGT_NORM_ras.tif                # Relatieve verwijzing naar het normenraster

[hoogtemodel]
bestand_pad = input/AHN/AHN4_WSA.tif                    # Relatieve verwijzing naar het hoogtemodel

[bgt]
bestand_pad = input/BGT/BGT.shp                         # Relatieve verwijzing naar de BGT shapefile
kolomnaam_functie = FUNCTIE                             # Kolomnaam in de BGT waarin de functie wordt beschreven
functie_pand = pand                                     # Functie in de BGT die panden beschrijven
functie_watervlak = waterloop, watervlak                # Functies in de BGT die water beschrijven, kommagescheiden

[peilgebieden]
bestand_pad = input/Shapefiles/PeilgebiedPraktijk.shp   # Relatieve verwijzing naar peilgebieden shapefile
kolomnaam_peilgebied_code = CODE                        # Kolomnaam in de peilgebiedenshape met peilgebiedcode
kolomnaam_peilgebied_peil_toetsing = WS_LAAGPEI         # Kolomnaam met peil te gebruiken voor toetsing
kolomnaam_peilgebied_peil_statistiek = WS_HOOGPEI       # Kolomnaam met peil te gebruiken voor bepaling initieel peil

[afwateringseenheden]
bestand_pad = input/Afwateringseenheden.shp             # Relatieve verwijzing naar afwateringseenheden shapefile
kolomnaam_afwateringseenheid_code = CODE                # Kolomnaam met de code van de afwateringseenheid
kolomnaam_peilgebied_code = PG_CODE                     # Kolomnaam met de code van het peilgebied waarin de KAE ligt
kolomnaam_peilgebied_peil_statistiek = WS_HOOGPEI       # Kolomnaam met peil te gebruiken voor bepaling initieel peil voor bepaling van statistieken

[percentages_toetshoogte]                               # Percentages te gebruiken voor de toetshoogte
10 = 5
11 = 10
25 = 1
50 = 1
100 = 0.1

[overig]
drempelhoogte_panden = 0.1                              # Aantal meter waarmee panden wordne opgehoogt
percentages = 0.1, 1, 2, 5, 10, 15, 20                  # Percentages van maaiveldhoogteklasse
kae_max_overlap_andere_peilgebieden = 0.01              # Fractie van een KAE waarmee een KAE met een ander peilgebied mag overlappen

```

### - settings_\<scenario>.ini -
```
[scenario]
naam = toekomstig                                   # Naam van het scenario
modelpakket = Sobek                                 # Type modelresultaat, kies uit [Sobek, D-Hydro]
his_file = input/lit/CALCPNT.HIS                    # SOBEK: Relatieve verwijzing naar de his file, of een kommagescheide lijst van his-file
ntw_file = input/lit/NETWORK.NTW                    # SOBEK: Relatieve verwijzing naar de ntw file
parameter = Waterlevel max. (m A                    # Naam van de parameter in de his-file die moet worden uitgelezen
ntw_nodes = SBK_GRIDPOINTFIXED, SBK_GRIDPOINT, SBK_CHANNELCONNECTION, SBK_CHANNEL_STORCONN&LAT # ntw-nodes die worden uitgelezen voor de waterstandsstatistiek

resultaat_folder = input/model/Output/              # D-Hydro hoofdmap waarin de verschillende events zijn weggeschreven
fou_max_wl_variabele = mesh1d_fourier002_max        # Naam van de variabele in de *_fou.nc file van de maximale waterstand
fou_max_wl_tijd_variabele = mesh1d_maximum002_time  # Naam van de variabele in de *_fou.nc file van het tijdstip van optreden van de maximale waterstand
exclude_boundary_nodes = True                       # D-Hydro: Zet op 'True' als rekenpunten met randvoorwaarden uitgefilterd moeten worden.
boundary_conditions_file = input/model/FlowFM_boundaryconditions1d.bc # D-Hydro: relatieve pad naar een .bc file

[toetshoogte]
bestand_pad = input/bbo_Toetshoogte_peilgebieden.shp #Verwijzing naar gecontroleerd bestand met toetshoogtes. Vaste kolomnamen nodig [T10, T10_GROEI, T25, T50, T100], nodata waarde is -999

[statistiek]
negeer_nodata = True                                # Verwijder rekenpunten waarvoor geen waterstandsstatistiek is uitgevoerd. Kies uit: True, False
negeer_nodes =                                      # Nodes die niet mee moeten worden genomen in de berekening van de waterstandsstatistiek. Bijvoorbeeld: exclude_nodes = id_node1, 10
plot_gumbel = False                                 # Plot gumbel grafieken, vertraagd het script. Kies uit: True, False
aantal_jaren_plotposities = 109                     # None of integer. Aantal jaren waarvoor de opgeven waterstandsreeks representatief is voor de Gumbel statistiek.
aggregatie_methode = median                         # Aggregatiemethode om waterstandspunten te aggregeren naar KAE. Kies uit: min, max, mean, median

[periode_groeiseizoen]
start_dag = 1                                       # Dag waarop het groeiseizoen start
start_maand = 3                                     # Maand waarop het groeiseizoen start
eind_dag = 1                                        # Dag waarop het groeiseizoen eindigt
eind_maand = 10                                     # Maand waarop het groeiseizoen eindigt

[handmatige_statistiek]                             # Indien 'bestand_pad' is ingevuld zal deze leidend zijn over de bovenstaande statistieksettings
bestand_pad =
kolomnaam_T10 = T10
kolomnaam_T10_GROEI = T10_GROEI
kolomnaam_T25 = T25
kolomnaam_T30 = T30
kolomnaam_T50 = T50
kolomnaam_T100 = T100

[dhydro_meteo]                                        # Optioneel: Voor D-Hydro modellen, exporteer .bui en .evp bestanden van de top n buien. 
event_overview_file = input/model/Buien/events.csv    # CSV bestand met overzicht van alle doorgerekende buien
event_folder = input/model/Buien                      # Map waarin alle .bui en .evp bestanden staan
export_top_n_events = 10                              # Minimaal aantal top events die worden geexporteerd
event_id_column = id                                  # Kolomnaam van de id-kolom. Als een bui '001.bui' heet moet in deze kolom ook '001' staan in plaats van '1'.
event_startdate_column = startdate                    # Startdatum van een bui in YYYY-MM-DD
event_enddate_column = enddate                        # Einddatum van een bui in YYYY-MM-DD

```

### Documentation
Documentation can be found [here](https://hhdelfland.visualstudio.com/ce76674e-d577-4ff0-8750-bd257ee91d7a/_apis/git/repositories/466ea3a5-b0ad-4d12-8e69-0583f0e1b142/items?path=/docs/Documentatie%20WSA%20toetsing.pdf&versionDescriptor%5BversionOptions%5D=0&versionDescriptor%5BversionType%5D=0&versionDescriptor%5Bversion%5D=main&resolveLfs=true&%24format=octetStream&api-version=5.0&download=true)

## Development
When working on the tool, clone the tool using git. Install the local tool by going to the main folder and using the command:
```pip install .```

### Deployment

Deployment over PyPi, using the following commands:

```
python setup.py sdist bdist_wheel
twine upload dist/*
```

If Twine is not yet installed, you can install this using:
```
pip install twine
```

Some versions of twine give the following issue:
```ERROR    InvalidDistribution: Invalid distribution metadata: unrecognized or malformed field 'license-file'```. A known working version of twine can be installed using:

```
pip install twine==6.0.1
```



## License
This project is licensed under the GNU GPLv3 License - see the LICENSE file for details.

## Attribution
This project uses hkvsobekpy