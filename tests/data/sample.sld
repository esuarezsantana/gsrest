<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor version="1.0.0"
    xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd"
    xmlns="http://www.opengis.net/sld"
    xmlns:ogc="http://www.opengis.net/ogc"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>wind_style</Name>
    <UserStyle>
      <Title>Wind speed</Title>
      <Abstract>Simple style for wind speed.</Abstract>
      <FeatureTypeStyle>
        <Rule>
          <RasterSymbolizer>
            <ColorMap>
              <ColorMapEntry color="#000000" opacity="0.0" quantity="-1.0" label="nodata"/>
              <ColorMapEntry color="#000000" opacity="1.0" quantity="0.0" label="zero(0)"/>
              <ColorMapEntry color="#ffffff" opacity="1.0" quantity="15.0" label="max(15)"/>
            </ColorMap>
            <ContrastEnhancement/>
          </RasterSymbolizer>
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
