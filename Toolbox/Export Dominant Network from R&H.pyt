import datetime
import os
import re
import time
import traceback

import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = 'Export Dominant Network'
        self.alias = 'rhdominant'

        # List of tool classes associated with this toolbox
        self.tools = [ExportDominantNetwork]



class ExportDominantNetwork(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Export Dominant Network from R&H"
        self.description = (
            'This tool will apply the concept of Route Dominance to the Enterprise Linear Referencing System, ' +
            'and it will export a network that includes just the "dominant" routes. The tool requires that the ' +
            'remove duplicate centerlines workflow has been executed to produce reliable results.'
        )
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        input_lrsn_fc = arcpy.Parameter(
            displayName='Input Route Network (LRSN Feature Class)',
            name='input_lrsn_fc',
            datatype='DEFeatureClass',
            direction='Input',
        )
        route_id_field = arcpy.Parameter(
            displayName='Route ID Field',
            name='route_id_field',
            datatype='GPString',
            parameterType='Required',
            direction='Input',
        )
        from_date_field = arcpy.Parameter(
            displayName='From Date Field',
            name='from_date_field',
            datatype='GPString',
            parameterType='Required',
            direction='Input',
        )
        to_date_field = arcpy.Parameter(
            displayName='To Date Field',
            name='to_date_field',
            datatype='GPString',
            parameterType='Required',
            direction='Input',
        )
        output_gdb = arcpy.Parameter(
            displayName='Output Workspace (File Geodatabase)',
            name='output_gdb',
            datatype='DEWorkspace',
            parameterType='Required',
            direction='Input',
        )
        temporal_view_date = arcpy.Parameter(
            displayName='Temporal View Date',
            name='temporal_view_date',
            datatype='GPDate',
            direction='Input',
        )
        save_intermediary_steps = arcpy.Parameter(
            displayName='Save Intermediary Steps to Disk',
            name='save_intermediary_steps',
            datatype='GPBoolean',
            parameterType='Optional',
            direction='Input',
        )
        validate_results = arcpy.Parameter(
            displayName='Check Output Network for Overlaps',
            name='validate_results',
            datatype='GPBoolean',
            parameterType='Optional',
            direction='Input'
        )
        overlapping_features = arcpy.Parameter(
            displayName='Overlapping Features (Feature Class)',
            name='overlapping_features',
            datatype='GPFeatureLayer',
            parameterType='Optional',
            direction='Input',
        )

        route_id_field.filter.type = 'ValueList'
        from_date_field.filter.type = 'ValueList'
        to_date_field.filter.type = 'ValueList'

        temporal_view_date.value = datetime.datetime.now()
        save_intermediary_steps.value = 'true'
        validate_results.value = 'true'

        return [
            input_lrsn_fc,
            route_id_field,
            from_date_field,
            to_date_field,
            output_gdb,
            temporal_view_date,
            save_intermediary_steps,
            validate_results,
        ]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        try:
            if arcpy.CheckExtension('highways') != 'Available':
                raise Exception
            arcpy.CalculateRouteConcurrencies_locref
            arcpy.MakeRouteEventLayer_lr
            arcpy.Erase_analysis
            arcpy.DeleteFeatures_management
        except Exception:
            return False
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if parameters[0].valueAsText:
            if not parameters[1].altered:
                rid_regex = re.compile('routeid|route_id')
                found_rid = False
                fields = arcpy.ListFields(parameters[0].valueAsText)
                parameters[1].filter.list = [field.name for field in fields if field.type == 'String']
                for field in fields:
                    if field.type == 'String':
                        field_name = field.name.lower()
                        if rid_regex.search(field_name):
                            index = fields.index(field)
                            parameters[1].value = fields[index].name
                            found_rid = True
                            break

            ## Look for commone FromDate field names in string type fields when the Input Route Network
            ## parameter is changed
            if not parameters[2].altered:
                from_date_regex = re.compile('from_date|fromdate')
                found_from_date = False
                fields = arcpy.ListFields(parameters[0].valueAsText)
                parameters[2].filter.list = [field.name for field in fields if field.type == 'Date']
                for field in fields:
                    if field.type == 'Date':
                        field_name = field.name.lower()
                        if from_date_regex.search(field_name):
                            index = fields.index(field)
                            parameters[2].value = fields[index].name
                            found_from_date = True
                            break

            if not parameters[3].altered:
            ## Look for commone ToDate field names in string type fields when the Input Route Network
            ## parameter is changed
                to_date_regex = re.compile('to_date|todate')
                found_to_date = False
                fields = arcpy.ListFields(parameters[0].valueAsText)
                parameters[3].filter.list = [field.name for field in fields if field.type == 'Date']
                for field in fields:
                    if field.type == 'Date':
                        field_name = field.name.lower()
                        if to_date_regex.search(field_name):
                            index = fields.index(field)
                            parameters[3].value = fields[index].name
                            found_to_date = True
                            break
        return
            # self.get_field_and_or_update_field_list(
            #     regex_text='routeid|route_id',
            #     param_index=1,
            # )
            # self.get_field_and_or_update_field_list(
            #     regex_text='fromdate|from_date',
            #     param_index=2,
            # )
            # self.get_field_and_or_update_field_list(
            #     regex_text='todate|to_date',
            #     param_index=3,
            # )
            ## Look for commone RouteId field names in string type fields when the Input Route Network
            ## parameter is changed

    # def get_field_and_or_update_field_list(self, regex_text, param_index, input_routes_index=0):
    #     regex = re.compile(regex_text)
    #     found_field = False
    #     fields = arcpy.ListFields(self.parameters[input_routes_index].valueAsText)
    #     for field in fields:
    #         if field.type in ['String', 'Date']:
    #             field_name = field.name.lower()
    #             if regex.search(field_name):
    #                 index = fields.index(field)
    #                 self.parameters[param_index].value = fields[index].name
    #                 found_field = True
    #                 break
    #     if not found_field:
    #         self.parameters[param_index].filter.list = [field.name for field in fields if field.type in ['String', 'Date']]
    #     return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        if parameters[0].value:
            input_gdb = os.path.dirname(parameters[0].valueAsText)
            orig_ws = arcpy.env.workspace
            arcpy.env.workspace = input_gdb
            if not arcpy.ListTables('*Lrs_Metadata'):
                parameters[0].setWarningMessage(
                    'Lrs_Metadata table was not found. It is required to run the Calculate Route Concurrencies ' +
                    'from the Location Referencing Toolbox, on which this tool depends. ' +
                    'Is the Input Route Network part of a R&H ALRS? It better be! ;-)' + str(arcpy.env.workspace) + str(arcpy.ListTables())
                )
                arcpy.env.workspace = orig_ws
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        input_lrsn_fc = parameters[0].valueAsText
        route_id_field_name = parameters[1].valueAsText
        from_date_field_name = parameters[2].valueAsText
        to_date_field_name = parameters[3].valueAsText
        output_gdb = parameters[4].valueAsText
        temporal_view_date = parameters[5].valueAsText
        save_intermediary_steps = parameters[6].valueAsText
        validate_results = parameters[7].valueAsText
        # overlaps_fc = parameters[5].valueAsText

        if save_intermediary_steps == 'true':
            save_intermediary_flag = True
        else:
            save_intermediary_flag = False

        if validate_results == 'true':
            validate_results_flag = True
        else:
            validate_results_flag = False

        tvd_list = temporal_view_date.split(' ')
        if len(tvd_list) == 1:
            tvd = datetime.datetime.strptime(temporal_view_date, r'%m/%d/%Y')
            concurrency_table = os.path.join(
                output_gdb,
                'RouteConcurrencies_{year}{month:02d}{day:02d}'.format(
                    year=tvd.year,
                    month=tvd.month,
                    day=tvd.day
                )
            )
        elif len(tvd_list) == 3:
            tvd = datetime.datetime.strptime(temporal_view_date, r'%m/%d/%Y %I:%M:%S %p')
            concurrency_table = os.path.join(
                output_gdb,
                'RouteConcurrencies_{year}{month:02d}{day:02d}_{hour:02d}{min:02d}{sec:02d}'.format(
                    year=tvd.year,
                    month=tvd.month,
                    day=tvd.day,
                    hour=tvd.hour,
                    min=tvd.minute,
                    sec=tvd.second
                )
            )
        else:
            raise ValueError(
                'The input Temporal View Date could not be parsed correctly. Try using the datepicker in the tool interface.'
            )

        try:
            arcpy.CheckOutExtension('highways')
            self.calculate_route_concurrencies(
                input_lrsn_fc,
                concurrency_table,
                tvd,
                messages
            )

            dominant_network_fc, delete_where_clause = self.make_dominant_network(
                input_lrsn_fc,
                concurrency_table,
                output_gdb,
                tvd,
                messages,
                save_intermediary_flag=save_intermediary_flag,
                lrsn_rid_field_name=route_id_field_name,
                lrsn_from_date_field_name=from_date_field_name,
                lrsn_to_date_field_name=to_date_field_name,
            )

            if validate_results_flag:
                overlaps_fc = os.path.join(
                    output_gdb,
                    os.path.basename(dominant_network_fc) + '_OVERLAPS'
                )
                self.check_for_overlaps(
                    dominant_network_fc,
                    overlaps_fc,
                    messages
                )
        except Exception as exc:
            messages.addErrorMessage('A(n) {} exception occurred. Checking in licenses and exiting.'.format(type(exc).__name__))
            arcpy.CheckInExtension('highways')
            messages.addErrorMessage(traceback.format_exc())
            raise exc

        arcpy.CheckInExtension('highways')

        messages.addWarningMessage('\nWARNING : It is highly recommended that you check the output Dominant Network for nonmonotonic features.')
        messages.addWarningMessage('WARNING : Use the Data Reviewer extension on the output feature class to check for nonmonotonic features.')
        if delete_where_clause:
            messages.addWarningMessage(
                '\nWARNING : The following where clause was used to delete features due to issues with the measures:\n' +
                '           {}'.format(delete_where_clause)
            )
        messages.addMessage('\nDominant network saved as: {}'.format(dominant_network_fc))

        return True

    def calculate_route_concurrencies(self, input_route_features, output_table, temporal_view_date, messages):
        messages.addMessage('Executing Calculate Route Concurrencies')
        messages.addMessage(' Input Route Features : {}'.format(input_route_features))
        messages.addMessage(' Output Table         : {}'.format(output_table))
        messages.addMessage(' Temporal View Date   : {}\n'.format(temporal_view_date))

        arcpy.CalculateRouteConcurrencies_locref(
            input_route_features,
            output_table,
            temporal_view_date
        )

        messages.addGPMessages()
        messages.addMessage('')

        return output_table

    def make_dominant_network(self, input_routes, concurrency_table, output_gdb, temporal_view_date, messages,
                              save_intermediary_flag=True, lrsn_rid_field_name='ROUTE_ID',
                              lrsn_from_date_field_name='FROM_DATE', lrsn_to_date_field_name='TO_DATE'):
        """
        After creating gaps in the input network where concurrencies exist,
        the geometries must be split to single parts. Then use the m-values
        from the single part geometries to create new routes. This is done to avoid
        non-monotonic routes. Non-monotonicity can be introduced from multipart
        outputs in GP tools, which are likely to reorder the part indices
        """
        # When the input_routes come from an RDBMS, it's possible the path to the table contains a `.`,
        # which arcpy doesn't support in FGDB. Always take the table name:
        lrsn_name = os.path.basename(input_routes).split('.')[-1]
        if save_intermediary_flag:
            routes_tvd_filtered = os.path.join(
                output_gdb,
                lrsn_name + '_tvd_filtered'
            )
            dom_table_path  = os.path.join(
                output_gdb,
                lrsn_name + '_dominant_table'
            )
            erased_routes_path = os.path.join(
                output_gdb,
                lrsn_name + '_concurr_gaps'
            )
            erased_routes_singlepart_path = os.path.join(
                output_gdb,
                lrsn_name + '_concurr_gaps_singlepart'
            )
            merged_routes_path = os.path.join(
                output_gdb,
                lrsn_name + '_dom_event_merge'
            )
        else:
            routes_tvd_filtered = os.path.join(
                'in_memory',
                lrsn_name + '_tvd_filtered_' + str(int(time.time()))
            )
            dom_table_path = os.path.join(
                'in_memory',
                lrsn_name + '_dominant_table_' + str(int(time.time()))
            )
            erased_routes_path = os.path.join(
                'in_memory',
                lrsn_name + '_concurr_gaps_' + str(int(time.time()))
            )
            erased_routes_singlepart_path = os.path.join(
                'in_memory',
                lrsn_name + '_concurr_gaps_singlepart_' + str(int(time.time()))
            )
            merged_routes_path = os.path.join(
                'in_memory',
                lrsn_name + '_dom_event_merge_' + str(int(time.time()))
            )

        dom_events_path = os.path.join(
            output_gdb,
            lrsn_name + '_dominant_event_' + str(int(time.time()))
        )

        output_path = os.path.join(
            output_gdb,
            lrsn_name + '_DOMINANT_NETWORK'
        )

        # Begin geoprocessing logic
        messages.addMessage('\nFiltering input routes to Temporal View Date: {}'.format(temporal_view_date))
        input_geodatabase = os.path.basename(
            os.path.dirname(
                input_routes
            )
        )
        split_geodatbase_name = os.path.splitext(input_geodatabase)
        if '.gdb' in split_geodatbase_name:
            base_active_routes_where_clause = (
                '({from_date} IS NULL OR {from_date} <= date \'{tvd}\') AND ({to_date} IS NULL OR {to_date} >= date \'{tvd}\')'
            )
        else:
            base_active_routes_where_clause = (
                '({from_date} IS NULL OR {from_date} <= \'{tvd}\') AND ({to_date} IS NULL OR {to_date} >= \'{tvd}\')'
            )

        active_routes_where_clause = (
            base_active_routes_where_clause.format(
                from_date=lrsn_from_date_field_name,
                tvd=temporal_view_date.strftime(r'%Y-%m-%d %H:%M:%S'),
                to_date=lrsn_to_date_field_name,
            )
        )
        messages.addMessage(' Using WHERE_CLAUSE:\n  {}'.format(active_routes_where_clause))
        routes_tvd_filtered_layer = arcpy.MakeFeatureLayer_management(
            input_routes,
            'routes_tvd_filtered_' + str(int(time.time())),
            where_clause=active_routes_where_clause
        )
        arcpy.CopyFeatures_management(
            routes_tvd_filtered_layer,
            routes_tvd_filtered
        )

        messages.addMessage('\nSubsetting concurrency table to only dominant events')
        where_clause = "(DominantFlag = 1) AND (DominantError <> 4)"
        messages.addMessage(' {}'.format(where_clause))
        arcpy.TableToTable_conversion(
            concurrency_table,
            os.path.dirname(dom_table_path),
            os.path.basename(dom_table_path),
            where_clause=where_clause
        )
        messages.addGPMessages()

        messages.addMessage('\nCreating event for route dominance')
        line_props = 'RouteId LINE FromMeasure ToMeasure'
        dom_layer = arcpy.MakeRouteEventLayer_lr(
            routes_tvd_filtered,
            lrsn_rid_field_name,
            dom_table_path,
            line_props,
            'dom_layer_' + str(int(time.time()))
        )
        if save_intermediary_flag:
            arcpy.CopyFeatures_management(
                dom_layer, dom_events_path
            )
            messages.addMessage(' {}'.format(dom_events_path))
        else:
            dom_events_path = dom_layer

        messages.addMessage('\nCreating network gaps at concurrencies')
        arcpy.Erase_analysis(routes_tvd_filtered, dom_events_path, erased_routes_path)
        messages.addGPMessages()

        messages.addMessage('\nSplitting gapped network to single-part geometries')
        arcpy.MultipartToSinglepart_management(
            erased_routes_path, erased_routes_singlepart_path
        )
        messages.addGPMessages()

        messages.addMessage('\nMerging dominant routes with gapped network')
        field_mapping = self.map_fields(
            [erased_routes_singlepart_path, lrsn_rid_field_name],
            [dom_events_path, 'RouteId'],
            lrsn_rid_field_name
        )
        arcpy.Merge_management(
            [erased_routes_singlepart_path, dom_events_path],
            merged_routes_path,
            field_mapping
        )
        messages.addGPMessages()

        messages.addMessage('\nAdding m-values to the merged routes attribute table')
        merged_field_names = [
            field.name for field in arcpy.ListFields(merged_routes_path)
        ]
        if not 'm_min' in merged_field_names:
            arcpy.AddField_management(
                merged_routes_path,
                'm_min',
                'DOUBLE',
            )
            messages.addGPMessages()
            messages.addMessage('')
        if not 'm_max' in merged_field_names:
            arcpy.AddField_management(
                merged_routes_path,
                'm_max',
                'DOUBLE',
            )
            messages.addGPMessages()

        measure_errors = []
        update_fields = ['SHAPE@', lrsn_rid_field_name, 'm_min', 'm_max']
        with arcpy.da.UpdateCursor(merged_routes_path, update_fields) as update_cursor:
            for row in update_cursor:
                shape = row[0]
                route_id = row[1]
                if not shape or not shape.extent:
                    m_min, m_max = None, None
                    measure_errors.append(route_id)
                else:
                    m_min = shape.extent.MMin
                    m_max = shape.extent.MMax
                update_cursor.updateRow([shape, route_id, m_min, m_max])
        messages.addMessage(' table update: complete')

        delete_where_clause = None # This variable becomes a string if there were features deleted.
        if measure_errors:
            messages.addWarningMessage(
                '\nThere are routes with invalid measure values! ' +
                'Deleting the following RouteIds from the output network:\n {}'.format(str(', '.join(measure_errors)))
            )

            delete_where_clause = '{} in (\''.format(lrsn_rid_field_name) + '\', \''.join(measure_errors) + '\')'
            merged_routes_delete_layer = arcpy.MakeFeatureLayer_management(
                merged_routes_path,
                'merged_routes_delete_layer_' + str(int(time.time()))
            )
            arcpy.SelectLayerByAttribute_management(
                merged_routes_delete_layer,
                selection_type='NEW_SELECTION',
                where_clause=delete_where_clause
            )
            if int(arcpy.GetCount_management(merged_routes_delete_layer).getOutput(0)) > 0:
                arcpy.DeleteFeatures_management(merged_routes_delete_layer)
                messages.addGPMessages()
                merged_routes_path = merged_routes_delete_layer
            else:
                messages.addWarningMessage('\nWARNING: Feature deletion failed!')

        messages.addMessage('\nCreating final network of only dominant routes')
        arcpy.CreateRoutes_lr(
            merged_routes_path,
            lrsn_rid_field_name,
            output_path,
            measure_source='TWO_FIELDS',
            from_measure_field='m_min',
            to_measure_field='m_max',
            build_index='INDEX',
        )
        messages.addGPMessages()

        # Try to clean up intermediary steps from memory if necessary
        if not save_intermediary_flag:
            try:
                orig_ws = arcpy.env.workspace
                arcpy.env.workspace = 'in_memory'
                temporary_fcs = arcpy.ListFeatureClasses()
                for fc in temporary_fcs:
                    try:
                        arcpy.Delete_management(fc)
                    except Exception as exc:
                        messages.addWarningMessage('{}: Failed to remove {} from memory'.format(
                            type(exc).__name__,
                            fc
                        ))
            except Exception:
                pass
            finally:
                arcpy.env.workspace = orig_ws

        return output_path, delete_where_clause

    def map_fields(self, table_field_a, table_field_b, output_name):
        field_mappings = arcpy.FieldMappings()

        field_map = arcpy.FieldMap()
        field_map.addInputField(*table_field_a)
        field_map.addInputField(*table_field_b)
        output_field = field_map.outputField
        output_field.name = output_name
        field_map.outputField = output_field
        field_mappings.addFieldMap(field_map)

        return field_mappings

    def check_for_overlaps(self, dominant_network_fc, overlaps_fc, messages):
        messages.addMessage('\nSearching for overlapping features in the output Dominant Network')
        arcpy.Intersect_analysis(
            dominant_network_fc,
            overlaps_fc,
        )
        messages.addGPMessages()
        messages.addMessage('')

        overlap_count = int(arcpy.GetCount_management(overlaps_fc).getOutput(0))
        
        if overlap_count == 0:
            messages.addMessage(
                '\nNo overlapping features were discovered. Removing the overlaps ' +
                'Feature Class from the Output GDB'
            )
            arcpy.Delete_management(overlaps_fc)
        else:
            messages.AddWarningMessage(
                '\n{count} features were written to the Overlaps Feature Class. '.format(
                    count=overlap_count,
                ) + 'There are likely {olaps} overlapping routes.'.format(
                    olaps=overlap_count/2
            ))
            messages.addWarningMessage(' Do you need to run the Remove Duplicate Centerlines process??')
            messages.addWarningMessage('Overlaps saved as: {}'.format(overlaps_fc))
        return
