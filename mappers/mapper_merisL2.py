#-------------------------------------------------------------------------------
# Name:        nansat_mapper_merisL2
# Purpose:     Mapping for Meris-L2 data
#
# Author:      antonk
#
# Created:     29.11.2011
# Copyright:   (c) asumak 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from vrt import VRT, Geolocation
from envisat import Envisat

class Mapper(VRT, Envisat):
    ''' Create VRT with mapping of WKV for MERIS Level 2 (FR or RR) '''

    def __init__(self, fileName, gdalDataset, gdalMetadata):

        product = gdalMetadata.get("MPH_PRODUCT", "Not_MERIS")

        if product[0:9] != "MER_FRS_2" and product[0:9] != "MER_RR__2":
            raise AttributeError("MERIS_L2 BAD MAPPER")

        # Get parameters for geolocation band
        #XSize, YSize, parameters = self.get_parameters(fileName, product[0:4], ["latitude", "zonal winds"])
        #
        # Create dataset with small band
        #geoDataset = VRT(srcRasterXSize=XSize, srcRasterYSize=YSize)
        #geoDataset._create_bands(parameters)
        #
        # Enlarge the band to the underlying data band size
        #self.geoDataset = geoDataset.resized(gdalDataset.RasterXSize, gdalDataset.RasterYSize)

        metaDict = [\
        {'source': fileName, 'sourceBand':  1, 'wkv': 'surface_ratio_of_upwelling_radiance_emerging_from_sea_water_to_downwelling_radiative_flux_in_air', 'parameters': {'wavelength': '412'} },\
        {'source': fileName, 'sourceBand':  2, 'wkv': 'surface_ratio_of_upwelling_radiance_emerging_from_sea_water_to_downwelling_radiative_flux_in_air', 'parameters': {'wavelength': '443'}},\
        {'source': fileName, 'sourceBand':  3, 'wkv': 'surface_ratio_of_upwelling_radiance_emerging_from_sea_water_to_downwelling_radiative_flux_in_air', 'parameters': {'wavelength': '490'}},\
        {'source': fileName, 'sourceBand':  4, 'wkv': 'surface_ratio_of_upwelling_radiance_emerging_from_sea_water_to_downwelling_radiative_flux_in_air', 'parameters': {'wavelength': '510'}},\
        {'source': fileName, 'sourceBand':  5, 'wkv': 'surface_ratio_of_upwelling_radiance_emerging_from_sea_water_to_downwelling_radiative_flux_in_air', 'parameters': {'wavelength': '560'}},\
        {'source': fileName, 'sourceBand':  6, 'wkv': 'surface_ratio_of_upwelling_radiance_emerging_from_sea_water_to_downwelling_radiative_flux_in_air', 'parameters': {'wavelength': '620'}},\
        {'source': fileName, 'sourceBand':  7, 'wkv': 'surface_ratio_of_upwelling_radiance_emerging_from_sea_water_to_downwelling_radiative_flux_in_air', 'parameters': {'wavelength': '665'}},\
        {'source': fileName, 'sourceBand':  8, 'wkv': 'surface_ratio_of_upwelling_radiance_emerging_from_sea_water_to_downwelling_radiative_flux_in_air', 'parameters': {'wavelength': '680'}},\
        {'source': fileName, 'sourceBand':  9, 'wkv': 'surface_ratio_of_upwelling_radiance_emerging_from_sea_water_to_downwelling_radiative_flux_in_air', 'parameters': {'wavelength': '708'}},\
        {'source': fileName, 'sourceBand': 10, 'wkv': 'surface_ratio_of_upwelling_radiance_emerging_from_sea_water_to_downwelling_radiative_flux_in_air', 'parameters': {'wavelength': '753'}},\
        {'source': fileName, 'sourceBand': 11, 'wkv': 'surface_ratio_of_upwelling_radiance_emerging_from_sea_water_to_downwelling_radiative_flux_in_air', 'parameters': {'wavelength': '761'}},\
        {'source': fileName, 'sourceBand': 12, 'wkv': 'surface_ratio_of_upwelling_radiance_emerging_from_sea_water_to_downwelling_radiative_flux_in_air', 'parameters': {'wavelength': '778'}},\
        {'source': fileName, 'sourceBand': 13, 'wkv': 'surface_ratio_of_upwelling_radiance_emerging_from_sea_water_to_downwelling_radiative_flux_in_air', 'parameters': {'wavelength': '864'}},\
        {'source': fileName, 'sourceBand': 15, 'wkv': 'mass_concentration_of_chlorophyll_a_in_sea_water', 'parameters': {'band_name': 'algal_1', 'case': 'I'} },\
        {'source': fileName, 'sourceBand': 16, 'wkv': 'volume_absorption_coefficient_of_radiative_flux_in_sea_water_due_to_dissolved_organic_matter', 'parameters': {'band_name': 'yellow_subs', 'case': 'II'} },\
        {'source': fileName, 'sourceBand': 17, 'wkv': 'mass_concentration_of_suspended_matter_in_sea_water', 'parameters': {'band_name': 'total_susp', 'case': 'II'} },\
        {'source': fileName, 'sourceBand': 18, 'wkv': 'mass_concentration_of_chlorophyll_a_in_sea_water', 'parameters': {'band_name': 'algal_2', 'case': 'II'} },\
        {'source': fileName, 'sourceBand': 22, 'wkv': 'quality_flags', 'parameters': {'band_name': 'l2_flags'} },\
        ];

        # add 'band_name' to 'parameters'
        for bandDict in metaDict:
            if bandDict['parameters'].has_key('wavelength'):
                bandDict['parameters']['band_name'] = 'reflectance_' + bandDict['parameters']['wavelength']

        #get GADS from header
        scales = self.read_scaling_gads(fileName, range(7, 20) + [20, 21, 22, 20])
        offsets = self.read_scaling_gads(fileName, range(33, 46) + [46, 47, 48, 46])
        # set scale/offset to the band metadata (only reflectance)
        for i, bandDict in enumerate(metaDict[:-1]):
            bandDict['parameters']['scale'] = str(scales[i])
            bandDict['parameters']['offset'] = str(offsets[i])

        #add geolocation dictionary into metaDict
        #for iBand in range(self.geoDataset.dataset.RasterCount):
        #    bandMetadata = self.geoDataset.dataset.GetRasterBand(iBand+1).GetMetadata()
        #    metaDict.append({'source': self.geoDataset.fileName, 'sourceBand': iBand+1, 'wkv': '', 'parameters':bandMetadata})

        # create empty VRT dataset with geolocation only
        VRT.__init__(self, gdalDataset);

        # add bands with metadata and corresponding values to the empty VRT
        self._create_bands(metaDict)

        # set time
        self._set_envisat_time(gdalMetadata)

        ''' Set GeolocationArray '''
        '''
        # Get parameters for geolocation band
        XSize, YSize, parameters = self.get_parameters(fileName, product[0:4], ["latitude", "longitude"])
        # Get geolocParameter (=[pixelOffset, linelOffset, pixelStep, lineStep])
        geolocParameter = self.get_GeoArrayParameters(fileName, product[0:4])

        # Create dataset with small band
        latlonVRT = VRT(srcRasterXSize=XSize, srcRasterYSize=YSize)
        latlonVRT._create_bands(parameters)

        # create dataset for longitude and
        for iBand in range(latlonVRT.dataset.RasterCount):
            band = latlonVRT.dataset.GetRasterBand(iBand+1)
            if band.GetMetadata()["band_name"] == "longitude":
                xBand = iBand+1
            elif band.GetMetadata()["band_name"] == "latitude":
                yBand = iBand+1

        self.add_geolocation(Geolocation(xVRT=latlonVRT.fileName,
                                  yVRT=latlonVRT.fileName,
                                  xBand=xBand, yBand=yBand,
                                  srs = gdalDataset.GetGCPProjection(),
                                  lineOffset = geolocParameter[1],
                                  lineStep = geolocParameter[3],
                                  pixelOffset = geolocParameter[0],
                                  pixelStep = geolocParameter[2]))
        '''