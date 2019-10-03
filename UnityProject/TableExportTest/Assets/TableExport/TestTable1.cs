//Create By Script
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
class TestTable1
{
	public enum Enum_EnumValue
	{
		E_TYPE1 = 0,
		E_TYPE2 = 1,
		E_TYPE3 = 2,
	}
	internal class TableData {
		public int Tid { get; }
		public string Name  { get; }
		public int IntValue { get; }
		public float FloatValue { get; }
		public Enum_EnumValue EnumValue { get; }
		public TableData(int tid, string name, int intvalue, float floatvalue, Enum_EnumValue enumvalue)
		{
			Tid = tid;
			Name = name;
			IntValue = intvalue;
			FloatValue = floatvalue;
			EnumValue = enumvalue;
		}
	}
	private static TestTable1 _instance;
	public static TestTable1 Get => _instance ?? (_instance = new TestTable1());
	private Dictionary<int, TableData> _dataDic = new Dictionary<int, TableData>();
	private TestTable1()
	{
		_dataDic[1001] = new TableData(1001, "表1数据1", 1, 1.2f, Enum_EnumValue.E_TYPE1);
		_dataDic[1002] = new TableData(1002, "表1数据2", 2, 1.4f, Enum_EnumValue.E_TYPE2);
		_dataDic[1003] = new TableData(1003, "表1数据3", 3, 1.6f, Enum_EnumValue.E_TYPE3);
		_dataDic[1004] = new TableData(1004, "表1数据4", 4, 1.8f, Enum_EnumValue.E_TYPE1);
		_dataDic[1005] = new TableData(1005, "表1数据5", 5, 2.0f, Enum_EnumValue.E_TYPE2);
		_dataDic[1006] = new TableData(1006, "表1数据6", 6, 2.2f, Enum_EnumValue.E_TYPE3);
		_dataDic[1007] = new TableData(1007, "表1数据7", 7, 2.4f, Enum_EnumValue.E_TYPE2);
	}
	public TableData GetData(int tid)
	{
		 return _dataDic[tid];
	}
}
