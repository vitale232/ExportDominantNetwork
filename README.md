Export Dominant Network from R&H
================================

Title  Export Dominant Network from R&H
---------------------------------------

Summary
-------

Exports only the dominant routes from a Roads and Highways ALRS. That is to say, in the event of a route concurrency, the subordinate route will be removed. This tool requires that dominance rules are established for the Roads and Highways Linear Referencing System Network (LRSN).

  

Usage
-----

*   Requires a Roads and Highways license
    
*   This tool currently only supports File Geodatabase and SQL Server geodatabases. Date queries may be handled differently on other RDBMS's.
    
*   This tool assumes you are following the R&H data model. Most importantly, ensure that your concurrent routes share a centerline (Use the Remove Duplicate Centerlines tool if required)
    
*   Outputs numerous files to disk (optional)
    
*   Requires that the Input Route Network is stored in a Roads and Highways geodatabase with an ALRS. This is due to the relieance of the Calculate Route Concurrencies tool in the Location Referencing toolbox on the ability to find the Lrs\_Metadata table.
    
*   The final dominant network will be the Input Route Network feature class name with the suffix "\_DOMINANT\_NETWORK", which can be found in the Output Geodatabase
    

For more information regarding the expected data schema, see the Esri Roads and Highways documentation: https://desktop.arcgis.com/en/arcmap/latest/extensions/roads-and-highways/alrs-data-model.htm

  

Syntax
------

ExportDominantNetwork\_rhutils (input\_lrsn\_fc, route\_id\_field, from\_date\_field, to\_date\_field, output\_gdb, temporal\_view\_date, {save\_intermediary\_steps}, {validate\_results})  
  

**Parameter**

**Explanation**

**Data Type**

input\_lrsn\_fc

Dialog Reference  

The input feature class, which must be a valid Roads and Highways Linear Referencing System Network (LRSN). Must be stored in a Roads and Highways database with a valid ALRS.

There is no python reference for this parameter.

Feature Class

route\_id\_field

Dialog Reference  

The name of the field on the Input Route Network that contains the R&H route IDs. Must be of type "String"

There is no python reference for this parameter.

String

from\_date\_field

Dialog Reference  

The name of the field on the Input Route Network that contains the R&H "from date". Must be of type "Date"

There is no python reference for this parameter.

String

to\_date\_field

Dialog Reference  

The name of the field on the Input Route Network that contains the R&H "todate". Must be of type "Date"

There is no python reference for this parameter.

String

output\_gdb

Dialog Reference  

The output location for the final dominant route network and, optionally, intermediary geoprocessing steps

There is no python reference for this parameter.

Workspace

temporal\_view\_date

Dialog Reference  

The temporal view date for the network.

There is no python reference for this parameter.

Date

save\_intermediary\_steps (Optional)

Dialog Reference  

If checked (the default), the various intermediary geoprocessing steps will be saved to the Output Geodatabase.

There is no python reference for this parameter.

Boolean

validate\_results (Optional)

Dialog Reference  

If checked (the default), the output Dominant Route Network will be analyzed with the Intersect Geoprocessing tool. If there are overlapping features found with the Intersect tool, they will be saved to the Output Geodatabase with the suffix "\_OVERLAPS". If there are none, the file will not appear in the Output Geodatabase.

There is no python reference for this parameter.

Boolean

Code Samples
------------

There are no code samples for this tool.

Tags
----

Roads and Highways, Linear Referencing, R&H, route dominance

Credits
-------

There are no credits for this item.

Use limitations
---------------

There are no access and use limitations for this item.