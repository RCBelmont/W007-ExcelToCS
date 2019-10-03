//Create By Script
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
class TestTable2
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
		public Enum_EnumValue EnumValue { get; }
		public float FloatValue { get; }
		public string[] StringValue { get; }
		public TableData(int tid, string name, int intvalue, Enum_EnumValue enumvalue, float floatvalue, string[] stringvalue)
		{
			Tid = tid;
			Name = name;
			IntValue = intvalue;
			EnumValue = enumvalue;
			FloatValue = floatvalue;
			StringValue = stringvalue;
		}
	}
	private static TestTable2 _instance;
	public static TestTable2 Get => _instance ?? (_instance = new TestTable2());
	private Dictionary<int, TableData> _dataDic = new Dictionary<int, TableData>();
	private TestTable2()
	{
		_dataDic[1001] = new TableData(1001, "表1数据1", 1, Enum_EnumValue.E_TYPE1, 1.2f, new[]{"aa", "aa"});
		_dataDic[1002] = new TableData(1002, "表1数据2", 2, Enum_EnumValue.E_TYPE2, 1.4f, new[]{"sdf", ""});
		_dataDic[1003] = new TableData(1003, "表1数据3", 3, Enum_EnumValue.E_TYPE3, 1.6f, new[]{"sdfe", "sdfe"});
		_dataDic[1004] = new TableData(1004, "表1数据4", 4, Enum_EnumValue.E_TYPE1, 1.8f, new[]{"sdfsd", "sdfsd"});
		_dataDic[1005] = new TableData(1005, "表1数据5", 5, Enum_EnumValue.E_TYPE2, 2.0f, new[]{"dsfsd", ""});
		_dataDic[1006] = new TableData(1006, "表1数据6", 6, Enum_EnumValue.E_TYPE3, 2.2f, new[]{"dsfsdf", "dsfsdf"});
		_dataDic[1007] = new TableData(1007, "表1数据7", 0, Enum_EnumValue.E_TYPE2, 2.4f, new[]{"dsfsdf", "dsfsdf"});
	}
	public TableData GetData(int tid)
	{
		 return _dataDic[tid];
	}
}
