from datetime import date, datetime
import PySimpleGUI as sg
import matplotlib.pyplot as plt


def compute_preOvertime(Hrs, HrlyPay):
    return Hrs * HrlyPay 
  
def compute_overtime(O_Hrs, HrlyPay):
    return O_Hrs * HrlyPay * 1.5 

def compute_netpay(G_pay):
    return round((G_pay * 0.9235) , 2)   #(Federal Payroll Tax for Social Secuirty/Medicare)
 
def render_chart (N_pay,tax):
    data = [N_pay , tax]
    gross_pay = N_pay + tax 
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    ax.pie(data, wedgeprops=dict(width=0.4), startangle=90)
    textstr = 'Net Pay  $%.2f' % (N_pay), 'Tax           $%.2f' % (tax)
    gross_info = 'Gross Pay   $%.2f' % (gross_pay)
    
    ax.text(-0.75, -1.2, gross_info, fontsize=10, 
    verticalalignment='center')
   
    ax.legend(textstr,
    loc="center left",
    bbox_to_anchor=(-0.8, 0.3, 0.5, 0.5),
    )
    ax.set_title(" Payroll Breakdown ")
    
    ax.annotate('7.65%',
            xy=(1, 1), xycoords='data',
            xytext=(0.1, 1.05),
            )
    
    ax.annotate('92.35%',
            xy=(1, 1), xycoords='data',
            xytext=(1.1, -0.2),
            )
    
    plt.show(block=False)

def write_recipt (FName, LName, E_ID, Hours, Otime, Wage, G_Pay, Tax, N_Pay):
    today = date.today().strftime("%m-%d-%y")
    fulldate = datetime.now().strftime("%m-%d-%y %H:%M:%S")
    file_name = (LName + '_Payroll_' + today + ".txt") 
    fullname = FName + ' ' + LName 
   
    # converts list into string 
    label = ["Employee ID" , "Regular Hours" , "Overtime" , "Wage", "Gross Pay", "Tax", "Net Pay"]
    joined_lab = ','.join([str(label) for label in label])
    split_lab = joined_lab.split(',')
    
    data_entry = [E_ID, Hours, Otime, Wage, G_Pay, Tax, N_Pay]
    joined_strings = ','.join([str(data_entry) for data_entry in data_entry])
    split_data = joined_strings.split(',')
     
    #formatting to concatenate label/data 
    a_zip = zip(split_lab, split_data) 
    zipped_list = str(list(a_zip))
    str_list_strip = str(zipped_list).strip("[]").strip("(").strip(")")
    str_list_replace = str_list_strip.replace(" ", "").replace(",", "").replace( ")(" , "\n").replace("''", ": ").replace("'", "")

    with open(file_name, "w") as f:
        f.write("Thanks for using Sully's Payroll Calculator. Here is your Reciept! \n")
        f.write("Reciept generated on " + fulldate + '\n\n')
        f.write("Full Name: " + fullname + '\n')
        f.write(str_list_replace)
        f.close()
      
def main():  
    layout = [  [sg.Image('ST_Logo.png' , size=(275, 85) )],
                [sg.Text('What is your First Name?',)],
                [sg.Input(size=(30,1), border_width = 3, key='-FName-')],
                [sg.Text('What is your Last Name?')], 
                [sg.Input(size=(30,1), border_width = 3, key='-LName-')],
                [sg.Text('What is your Employee ID?')], 
                [sg.Input(size=(30,1), border_width = 3, key='-E_ID-', enable_events=True)],
                [sg.Text('Regular Hours Worked  '), sg.Input(size=(8,1), enable_events=True, border_width = 3, key='-Hours-')], 
                [sg.Text('Overtime Hours Worked'), sg.Input(size=(8,1), enable_events=True, border_width = 3, key='-Overtime-')],
                [sg.Text('Hourly Payrate                 '), sg.Input(size=(8,1), enable_events=True, border_width = 3,  key='-Wage-')],
                [sg.Text('Gross Pay                        '), sg.Text(size=(10,1), key='-GPay_Out-')],
                [sg.Text('Tax Witheld                      '), sg.Text(size=(10,1), key='-Tax_Out-')],
                [sg.Text('Net Pay                             '), sg.Text(size=(10,1), key='-NPay_Out-')],
                [sg.Text(''), sg.Text(size=(35,1), key='-Message-')],
                [sg.Button('Calculate', button_color = '#2ad624'), 
                 sg.Button('Plot', button_color = '#076cfa'),
                 sg.Button('Receipt', button_color = '#3434d9'),
                 sg.Button('Clear', button_color = ('black','#b8433b'))],
                ]
    
    sg.theme('DarkBlue3')            
    window = sg.Window("Sully's Payroll Calculator", layout, size= (310,525), font = ("Helvetica",12), resizable=True, finalize=True)

    while True:            
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Calculate':
            try:
                hours = int(values['-Hours-'])
                overtime = int(values['-Overtime-'])
                wage_float = float(values['-Wage-'])
                wage = round(wage_float,2)
                
                pay_beforeOvertime = compute_preOvertime(hours, wage)
                pay_withOvertime = pay_beforeOvertime + compute_overtime(overtime, wage)
                gross_pay = round(pay_withOvertime,2) 
                net_pay = compute_netpay(gross_pay)
                tax_witheld_float = gross_pay - net_pay
                tax_witheld = round(tax_witheld_float,2)
                window['-GPay_Out-'].update(f'${gross_pay:.2f}', background_color = '#43b57a', text_color = 'black')
                window['-Tax_Out-'].update(f'  ${tax_witheld:.2f}', background_color = '#d7e817', text_color = 'black')
                window['-NPay_Out-'].update(f'${net_pay:.2f}' , background_color = '#00ff37', text_color = 'black')
                window['-Message-'].update( '', background_color = '#64778d')    
            except:
                window['-Message-'].update('Please input fields', text_color = 'black', background_color = "yellow")  
        if event == 'Plot':
            try:
                render_chart(net_pay,tax_witheld)
            except: 
                window['-Message-'].update('Please calculate before plot', text_color = 'black', background_color = "yellow")
        if event == 'Clear':    
            keys_to_clear = '-FName-', '-LName-', '-E_ID-', '-Hours-', '-Overtime-', '-Wage-', '-GPay_Out-', '-Tax_Out-', '-NPay_Out-', '-Message-'
            clear_highlight = '-GPay_Out-', '-Tax_Out-', '-NPay_Out-', '-Message-'
        
            for key in clear_highlight:
                window[key].update(background_color = '#64778d')
            for key in keys_to_clear:
                window[key].update('')
            plt.close()    
           
        # User Input Validation    
        if event == '-E_ID-' and values['-E_ID-'] and values['-E_ID-'][-1] not in ('1234567890') or len(values['-E_ID-']) > 7 :
           window['-E_ID-'].update(values['-E_ID-'][:-1]) 
        if event == '-Hours-' and values['-Hours-'] and values['-Hours-'][-1]  not in ('1234567890') or len(values['-Hours-']) > 3:
            window['-Hours-'].update(values['-Hours-'][:-1])
        if event == '-Overtime-' and values['-Overtime-'] and values['-Overtime-'][-1]  not in ('1234567890') or len(values['-Overtime-']) > 3:
            window['-Overtime-'].update(values['-Overtime-'][:-1])     
        if event == '-Wage-' and values['-Wage-'] and values['-Wage-'][-1]  not in ('1234567890.') or len(values['-Wage-']) > 6:
            window['-Wage-'].update(values['-Wage-'][:-1])  
            
        if event == 'Receipt':   
            try:
                fname = (values['-FName-'])
                lname = (values['-LName-'])
                e_id =  (values['-E_ID-']) 
                write_recipt(fname, lname, e_id, hours, overtime, wage, gross_pay, tax_witheld, net_pay) 
                window['-Message-'].update('Receipt Succesfully Created!', text_color = 'black', background_color = "#9934ba")
            except:      
                window['-Message-'].update('Please calculate before receipt', text_color = 'black', background_color = "yellow")           
    
    window.close()

if __name__ == '__main__':
    main()
    



