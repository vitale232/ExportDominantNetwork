# Export Dominant Network from R&H

This tool is designed to remove the non-dominant routes from an Esri ArcGIS Desktop Roads and Highways Advanced Linear Referencing System (ALRS/LRS). The Roads and Highways data model allows for route concurrencies, which are two roadway features that overlap one another. For reporting purposes, overlapping roadways are generally considered as a single piece of pavement. Thus, simply summing the calibrated length of the route features will lead to an over-estimation of the centerline miles present.

This relies on the assumption that your data uses Route Dominance, a Roads and Highways concept, and that you have an ALRS that is built to the [R&H Data Model specification](https://desktop.arcgis.com/en/arcmap/latest/extensions/roads-and-highways/alrs-data-model.htm) 

Mostly, we are assuming that concurrent routes are built using the same centerline, and that you have Route Dominance enabled and configured such that you will not have a dominance tie (i.e. two routes are equivalent given the dominance rules).

# Tool documentation

This documentation is also available in the Geoprocessing Tool GUI.

Summary
-------

Exports only the dominant routes from a Roads and Highways ALRS. That is to say, in the event of a route concurrency, the subordinate route will be removed. This tool requires that dominance rules are established for the Roads and Highways Linear Referencing System Network (LRSN).

Usage
-----

*   Requires a Roads and Highways license
    
*   This tool currently only supports File Geodatabase and SQL Server geodatabases. Date queries may be handled differently on other RDBMS's.
    
*   This tool assumes you are following the R&H data model. Most importantly, ensure that your concurrent routes share a centerline (Use the Remove Duplicate Centerlines tool if required)
    
*   Outputs numerous files to disk (optional)
    
*   Requires that the Input Route Network is stored in a Roads and Highways geodatabase with an ALRS. This is due to the reliance of the Calculate Route Concurrencies tool in the Location Referencing toolbox on the ability to find the Lrs\_Metadata table.
    
*   The final dominant network will be the Input Route Network feature class name with the suffix "\_DOMINANT\_NETWORK", which can be found in the Output Geodatabase
    

For more information regarding the expected data schema, see the Esri Roads and Highways documentation: https://desktop.arcgis.com/en/arcmap/latest/extensions/roads-and-highways/alrs-data-model.htm

Syntax
------

ExportDominantNetwork\_rhdominant (input\_lrsn\_fc, route\_id\_field, from\_date\_field, to\_date\_field, output\_gdb, temporal\_view\_date, {save\_intermediary\_steps}, {validate\_results})  
  


**input\_lrsn\_fc**

The input feature class, which must be a valid Roads and Highways Linear Referencing System Network (LRSN). Must be stored in a Roads and Highways database with a valid ALRS.


**route\_id\_field**

The name of the field on the Input Route Network that contains the R&H route IDs. Must be of type "String"

**from\_date\_field**

The name of the field on the Input Route Network that contains the R&H "from date". Must be of type "Date"

**to\_date\_field**

The name of the field on the Input Route Network that contains the R&H "to date". Must be of type "Date"

**output\_gdb**

The output location for the final dominant route network and, optionally, intermediary geoprocessing steps

**temporal\_view\_date**

The temporal view date for the network.

**save\_intermediary\_steps (Optional)**

If checked (the default), the various intermediary geoprocessing steps will be saved to the Output Geodatabase.

**validate\_results (Optional)**

If checked (the default), the output Dominant Route Network will be analyzed with the Intersect Geoprocessing tool. If there are overlapping features found with the Intersect tool, they will be saved to the Output Geodatabase with the suffix "\_OVERLAPS". If there are none, the file will not appear in the Output Geodatabase.


Tags
----

Roads and Highways, Linear Referencing, R&H, route dominance

Credits
-------

There are no credits for this item.

Use limitations
---------------

This tool requires the Roads and Highways extension for ArcGIS. It's only known to work when the **Input Routes Network** is in a file geodatabase or a SQL Server 2016 SDE relational database. It also requires elevated licenses to access some geoprocessing tools.

# Installation
## With Git
If you have a git client installed on your computer, you can clone the repository using the following command:

```bash
git clone https://github.com/vitale232/ExportDominantNetwork.git
```

Once the repository is cloned, simply navigate to the `./Toolbox` directory using ArcGIS Desktop or ArcCatalog, and you should see a toolbox called "Export Dominant Network from R&H.pyt". Expand the toolbox, double click the tool, and you should be good to go.

## Without Git

If you do not have git, you can click on the green "Clone or Download" button towards the top of this page. Select the "Download Zip" option. When the download is complete, unzip the directory onto your computer, navigate to the `./Toolbox` directory using ArcGIS Desktop or ArcCatalog, and you should see a toolbox called "Export Dominant Network from R&H.pyt". Expand the toolbox, double click the tool, and you should be good to go.

## Moving the Tool from the Repository

The tool does not need to remain in the git repository. If you want to move the tool from the `./Toolbox` directory, be sure to keep all of the contents of the `Toolbox` directory together. If the `.pyt` file and the `.xml` files are not kept together, the tools documentation will not work.

# Repository Structure

## ./Toolbox
The `./Toolbox` directory contains the [Python Toolbox](https://desktop.arcgis.com/en/arcmap/10.5/analyze/creating-tools/a-quick-tour-of-python-toolboxes.htm)

The file with the `.pyt` tool is written in `Python 2.7.13` syntax. The `.pyt` extension allows the ArcGIS Python interpreter know it can expect a certain class structure, so that it can construct the GUI.

The `.xml` files are the documentation for the tool. Keep the tool and the documentation in the same directory, so that the `Show Help` and `Tool Help` buttons work correctly in the ArcGIS Desktop Geoprocessing Tool GUI.

## ./DataReviewer

The `./DataReviewer` directory contains a file called `nonmon.rbj`. This is a reviewer batch job that will execute the Non-Monotonic Polyline Data Reviewer check via a batch job. The Data Reviewer extension is included with Roads and Highways. It is highly suggested you run the Non-Monotonic Polyline Data Reviewer check on the output network to ensure the geoprocessing hasn't messed up route calibration.
