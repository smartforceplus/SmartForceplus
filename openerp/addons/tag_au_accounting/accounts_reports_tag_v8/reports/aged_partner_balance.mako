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
    <table width="100%" style="border-collapse: collapse"border=1>
      <tr>
        <td style="font-weight:bold;text-align:center;">
          Chart of Accounts
        </td>
        <td style="font-weight:bold;text-align:center;">
          Fiscal Year
        </td>
        <td style="font-weight:bold;text-align:center;">
          Start Date
        </td>
        <td style="font-weight:bold;text-align:center;">
          Period Length(days)
        </td>
        <td style="font-weight:bold;text-align:center;">
          Partner's
        </td>
        <td style="font-weight:bold;text-align:center;">
          Analysis Direction
        </td>
        <td style="font-weight:bold;text-align:center;">
          Target Moves
        </td>
      </tr>
        <tr>
        <td style="text-align:center">
          ${get_account(data) or '' }
        </td>
        <td style="text-align:center">
          ${get_fiscalyear(data) or '' }
        </td>
        <td style="text-align:center">
          ${formatLang(data['form']['date_from'],date=True) }
        </td>
        <td style="text-align:center">
          ${data['form']['period_length'] }
        </td>
        <td style="text-align:center">
          ${get_partners(data) }
        </td>
        <td style="text-align:center">
          ${data['form']['direction_selection'] }
        </td>
        <td style="text-align:center">
          ${get_target_move(data) }
        </td>
      </tr>
      </table>
      <br/><br/><hr color="black"/>
    <table width="100%">
      <tr>
        <td style="font-weight:bold;text-align:left;">
          Partners
        </td>
        <td style="font-weight:bold;text-align:right">
          ${data['form']['direction_selection'] == 'future' and 'Due' or 'Not due' }
        </td>
        <td style="font-weight:bold;text-align:right">
          ${data['form']['4']['name'] }
        </td>
        <td style="font-weight:bold;text-align:right">
          ${data['form']['3']['name'] }
        </td>
        <td style="font-weight:bold;text-align:right">
          ${data['form']['2']['name'] }
        </td>
        <td style="font-weight:bold;text-align:right">
          ${data['form']['1']['name'] }
        </td>
        <td  style="font-weight:bold;text-align:right">
          ${data['form']['0']['name'] }
        </td>
        <td style="font-weight:bold;text-align:right">
          Total
        </td>
      </tr>
      
      <tr>
        <td style="font-weight:bold;text-align:left;border-bottom: 1px solid black">
        <%
        	partner = get_lines(data['form'])
        	not_partner = get_lines_with_out_partner(data['form'])
        %>Account Total
        </td>
        <td style="font-weight:bold;text-align:right;border-bottom: 1px solid black">
          ${formatLang(get_direction('6'))}
        </td>
        <td style="font-weight:bold;text-align:right;border-bottom: 1px solid black">
          ${formatLang(get_for_period('4'))}
        </td>
        <td style="font-weight:bold;text-align:right;border-bottom: 1px solid black">
          ${formatLang(get_for_period('3'))}
        </td>
        <td style="font-weight:bold;text-align:right;border-bottom: 1px solid black">
          ${formatLang(get_for_period('2'))}
        </td>
        <td style="font-weight:bold;text-align:right;border-bottom: 1px solid black">
          ${formatLang(get_for_period('1'))}
        </td>
        <td style="font-weight:bold;text-align:right;border-bottom: 1px solid black">
          ${formatLang(get_for_period('0'))}
        </td>
        <td style="font-weight:bold;text-align:right;border-bottom: 1px solid black">
          ${formatLang(get_total('5'))}
        </td>
      </tr>
      
	  % for partner in get_lines(data['form']):
      <tr>
        <td>
          ${partner['name'] or ''}        
        </td>
        <td style="text-align:right">
          ${formatLang(partner['direction'])}
        </td>
        <td style="text-align:right">
          ${formatLang(partner['4'])}
        </td>
        <td style="text-align:right">
          ${formatLang(partner['3'])}
        </td>
        <td style="text-align:right">
          ${formatLang(partner['2'])}
        </td>
        <td style="text-align:right">
          ${formatLang(partner['1'])}
        </td>
        <td style="text-align:right">
          ${formatLang(partner['0'])}
        </td>
        <td style="text-align:right">
          ${formatLang(partner['total'])}
        </td>
      </tr>
      %endfor
      % for not_partner in get_lines_with_out_partner(data['form']):
      <tr>
        <td>
          ${not_partner['name'] }
        </td>
        <td style="text-align:right">
          ${formatLang(not_partner['direction'])}
        </td>
        <td style="text-align:right">
          ${formatLang(not_partner['4'])}
        </td>
        <td style="text-align:right">
          ${formatLang(not_partner['3'])}
        </td>
        <td style="text-align:right">
          ${formatLang(not_partner['2'])}
        </td>
        <td style="text-align:right">
          ${formatLang(not_partner['1'])}
        </td>
        <td style="text-align:right">
          ${formatLang(not_partner['0'])}
        </td>
        <td style="text-align:right">
          ${formatLang(not_partner['total'])}
        </td>
      </tr>
      %endfor
    </table>
</body>
</html>