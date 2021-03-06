﻿using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace PyCT
{
    public class Adapter
    {
        private WebServices.GUI guiService;

        private string password;

        public string URL
        {
            get
            {
                return this.guiService.Url;
            }
            set
            {
                this.guiService.Url = value;
            }
        }

        public string Username { get; set; }

        public string Password
        {
            get
            {
                return this.password;
            }
            set
            {
                SHA1 hash = new SHA1Managed();
                this.password = Convert.ToBase64String(hash.ComputeHash(UTF8Encoding.UTF8.GetBytes(value)));
            }
        }

        public Adapter(string username, string password, string url = null)
        {
            this.guiService = new WebServices.GUI();
            if (!string.IsNullOrEmpty(url)) this.guiService.Url = url;
            this.Username = username;
            this.Password = password;
            this.guiService.Timeout = System.Threading.Timeout.Infinite;
            this.guiService.EnableDecompression = true;
        }

        public DataSet Validate() {
            return this.guiService.ValidateLogin(false, this.Username, this.Password);
        }

        public DataSet GetData(string dataView, string parms, int offset, int limit)
        {
            DataSet dataSet = this.guiService.GetData(
                false, this.Username, this.Password, dataView, parms, offset, limit, null);
            if (dataSet.Tables.Contains(dataView)) 
            {
                ApplyConstraints(dataSet.Tables[dataView]);
            }
            return dataSet;
        }

        public void ApplyConstraints(DataTable dataTable)
        {
            if (dataTable != null &&
                dataTable.Columns != null &&
                dataTable.Columns.Count > 0)
            {
                foreach (DataColumn dc in dataTable.Columns)
                {
                    if (
                        dc.ExtendedProperties.Contains("is_primary_key") 
                        && dc.ExtendedProperties["is_primary_key"].ToString() == "Y"
                    )
                    {
                        if (dc.DataType == typeof(int))
                        {
                            dc.AllowDBNull = false;
                            dc.AutoIncrement = true;
                            dc.AutoIncrementSeed = -1;
                            dc.AutoIncrementStep = -1;
                            dataTable.PrimaryKey = new DataColumn[1] { dc };
                        }
                        else
                        {
                            dc.AllowDBNull = false;
                            dataTable.PrimaryKey = new DataColumn[1] { dc };
                        }
                    }
                }
            }
        }
    }
}
