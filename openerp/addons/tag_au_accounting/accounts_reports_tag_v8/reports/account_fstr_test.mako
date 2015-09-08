<html>
<head>
<style type="text/css">
	    .basic_table
	    {
	      text-align:center;
	      border:1px solid lightGrey;
	      border-collapse: collapse;
	    } 
	    .basic_table td
	    {
	    border:1px solid lightGrey;
	    font-size:12;
	    }
	    .list_table
	    {
	    border-color:black;
	    text-align:center;
	    border-collapse:collapse;
	    }
	    .list_table td
	    {
	    border-color:gray;
	    border-top:1px solid gray;
	    text-align:left;
	    font-size:12;
	    padding-right:3px padding-left:3px padding-top:3px padding-bottom:3px
	    }
	    .list_table th
	    {
	    border-bottom:2px solid black;
	    text-align:left;
	    font-size:12;
	    font-weight:bold;
	    padding-right:3px padding-left:3px
	    }
	    .list_tabe thead
	    {
	    display:table-header-group;
	    }
	    .total
	    {
	    width:100%;
	    }
	    .tax
	    {
	    width:50%;
	    }
	    .act_as_table
	    {
	    display: table;
	    }
	    .act_as_row
	    {
	    display: table-row;
	    }
	    .act_as_cell
	    {
	    display: table-cell;
	    }
	    .act_as_thead
	    {
	    display: table-header-group;
	    }
	    .act_as_tbody
	    {
	    display: table-row-group;
	    }
	    .act_as_tfoot
	    { 
	    display: table-footer-group;
	    }
	    .act_as_caption
	    {
	    display: table-caption;
	    }
	    act_as_colgroup
	    {
	    display: table-column-group;
	    }
	    .list_table, .data_table
	    {
	    width: 100%;
	    table-layout: fixed
	    }
	    .bg, .act_as_row.labels
	    {
	    background-color:#F0F0F0;
	    }
	    .list_table, .data_table, .list_table .act_as_row
	    {
	    border-left:0px;
	    border-right:0px;
	    text-align:left;
	    font-size:9px;
	    padding-right:3px;
	    padding-left:3px;
	    padding-top:2px;
	    padding-bottom:2px;
	    border-collapse:collapse;
	    }
	    .list_table .act_as_row.labels, .list_table .act_as_row.initial_balance, .list_table .act_as_row.lines
	    {
	    border-color:gray;
	    border-bottom:1px solid lightGrey;
	    }
	    .data_table .act_as_cell
	    {
	    border: 1px solid lightGrey;
	    text-align: center;
	    }
	    .data_table .act_as_cell, .list_table .act_as_cell
	    {
	    word-wrap: break-word;
	    }
	    .data_table .act_as_row.labels
	    {
	    font-weight: bold;
	    }
	    .initial_balance .act_as_cell
	    {
	    font-style:italic;
	    }
	    .account_title
	    {
	    font-size:10px;
	    font-weight:bold;
	    page-break-after: avoid;
	    }
	    .act_as_cell.amount
	    {
	    word-wrap:normal; text-align:right;
	    }
	    .list_table .act_as_cell
	    {
	    padding-left: 5px;
	    border-right:1px solid lightGrey;
	    }
	    .list_table .act_as_cell.first_column
	    {
	    padding-left: 0px;
	    border-left:1px solid lightGrey; uncomment to active column lines
	    }
	    .account_level_1
	    {
	    text-transform: uppercase;
	    /*font-weight: bold;*/
	    font-size: 15px;
	    background-color:#F0F0F0;
	    }
	    /*
	    .account_level_1 .act_as_cell
	    {
	    height: 30px;
	    vertical-align: bottom;
	    } */
	    .account_level_2
	    {
	    /*text-transform: uppercase;
	    font-weight: bold;
	    */
	    font-size: 12px;
	    background-color:#F0F0F0;
	    }
	    /*
	    .account_level_2 .act_as_cell
	    {
	    height: 20px;
	    vertical-align: bottom;
	    }
	    .account_level_3
	    {
	    text-transform: uppercase;
	    font-weight: bold;
	    font-size: 11px;
	    background-color:#FAFAFA;
	    }
	    .account_level_4
	    {
	    font-weight: bold;
	    font-size: 11px;
	    }
	    */
	    .account_level_5 { }
	    .regular_account_type
	    {
	    font-weight: normal;
	    }
	    .view_account_type
	    {
	    font-weight: bold;
	    }
	    .account_level_consol
	    {
	    font-weight: normal;
	    font-style: italic;
	    }
	    .act_as_table_emipro
	    {
	    font-size:15px !important;
	    color:red !important;
	    }
	</style>
</head>

<body onload="changeheight();">
	<!--Main for start-->
    %for o in objects :
    	<center><span class="title" style = "font-size:19pt;"><b>${ template_data['name'] or '' }</b></span></center>
    	</br></br>
    	<!--Child for start-->
    	<table width = "100%">
    	% for obj in template_data['statements'][0]:
    		<tr>
    		<td style="padding-left:${obj.get('indent') or 0}px">${obj.get('name') or 'Error'}</td>
    		% if '(' in obj.get('total_amount'):
    			<td style="text-align:right;color:red">${obj.get('total_amount') or 'Error'}</td>
    		%else:
    			<td style="text-align:right">${obj.get('total_amount') or 'Error'}</td>
    		%endif
    		</tr>
    	<!--Child for over-->
    	%endfor
    	</table>
    <!--Main for over-->
    <br/><hr/>
    %endfor
    
    
    
</body>
</html>