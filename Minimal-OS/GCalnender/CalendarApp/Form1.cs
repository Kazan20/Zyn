using System;
using System.Windows.Forms;

namespace CalendarApp
{
    public partial class Form1 : Form
    {
        private MonthCalendar monthCalendar1;

        public Form1()
        {
            InitializeComponent();
            InitializeMonthCalendar();
        }

        private void InitializeMonthCalendar()
        {
            this.monthCalendar1 = new MonthCalendar();
            this.monthCalendar1.Location = new System.Drawing.Point(13, 13);
            this.monthCalendar1.Name = "monthCalendar1";
            this.monthCalendar1.TabIndex = 0;
            this.monthCalendar1.DateChanged += new DateRangeEventHandler(this.MonthCalendar1_DateChanged);
            this.Controls.Add(this.monthCalendar1);
        }

        private void MonthCalendar1_DateChanged(object sender, DateRangeEventArgs e)
        {
            // Display the selected date in a message box
            MessageBox.Show("Selected Date: " + monthCalendar1.SelectionStart.ToShortDateString());
        }
    }
}
