


using System;
using System.Collections.Generic;
using System.Security.Cryptography.X509Certificates;

class TableName
{
    public enum MyEnum
    {
        GG = 1   
    }
    private static TableName _instance;
    public static TableName Get => _instance ?? (_instance = new TableName());
    private Dictionary<int, TableData> _dataDic = new Dictionary<int, TableData>();
    private List<MyEnum> AA;
    internal class TableData
    {
        public int Tid { get; }
        private MyEnum[] d;
        public TableData(MyEnum[] aa)
        {
            d = aa;
        }
    }

    private TableName()
    {
        int[] a = new[] {1, 2, 3};
        new TableData(new []{(MyEnum.GG)});
    }

    public TableData GetData(int tid)
    {
        return _dataDic[tid];
    }
}