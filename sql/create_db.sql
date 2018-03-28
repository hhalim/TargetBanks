/****** Object:  Database [bkrob]    Script Date: 3/27/2018 4:33:45 PM ******/
CREATE DATABASE [bkrob]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'bkrob', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL13.SQL2016\MSSQL\DATA\bkrob.mdf' , SIZE = 73728KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'bkrob_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL13.SQL2016\MSSQL\DATA\bkrob_log.ldf' , SIZE = 139264KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
GO

USE [bkrob]
GO

/****** Object:  Table [dbo].[Bank]    Script Date: 3/27/2018 4:32:13 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Bank](
	[BankID] [int] IDENTITY(1,1) NOT NULL,
	[UniqueNum] [varchar](50) NULL,
	[Name] [varchar](100) NULL,
	[Address1] [varchar](100) NULL,
	[Address2] [varchar](100) NULL,
	[City] [varchar](100) NULL,
	[State] [varchar](2) NULL,
	[Zip] [varchar](20) NULL,
	[Deposit] [bigint] NULL,
	[Lat] [float] NULL,
	[Lng] [float] NULL,
	[ClosestStationID] [int] NULL,
	[ClosestPSDistance] [float] NULL,
	[MeanPSDistance] [float] NULL,
	[PSCount] [int] NULL,
	[Take] [bigint] NULL,
	[PDistance] [float] NULL,
	[Officers1000] [float] NULL,
	[FFLCount] [int] NULL,
	[AvgRating] [float] NULL,
	[Target] [int] NULL,
 CONSTRAINT [PK_Bank] PRIMARY KEY CLUSTERED 
	(
		[BankID] ASC
	)
) ON [PRIMARY]
GO

CREATE TABLE [dbo].[BankSample](
	[BankID] [int] NOT NULL,
	[UniqueNum] [varchar](50) NULL,
	[Name] [varchar](100) NULL,
	[Address1] [varchar](100) NULL,
	[Address2] [varchar](100) NULL,
	[City] [varchar](100) NULL,
	[State] [varchar](2) NULL,
	[Zip] [varchar](20) NULL,
	[Deposit] [bigint] NULL,
	[Lat] [float] NULL,
	[Lng] [float] NULL,
	[ClosestStationID] [int] NULL,
	[ClosestPSDistance] [float] NULL,
	[MeanPSDistance] [float] NULL,
	[PSCount] [int] NULL,
	[Take] [bigint] NULL,
	[PDistance] [float] NULL,
	[Officers1000] [float] NULL,
	[FFLCount] [int] NULL,
	[AvgRating] [float] NULL,
	[Target] [int] NULL,
 CONSTRAINT [PK_BankSample] PRIMARY KEY CLUSTERED 
	(
		[BankID] ASC
	)
) ON [PRIMARY]
GO

CREATE TABLE [dbo].[CrimeRate](
	[CrimeRateID] [int] IDENTITY(1,1) NOT NULL,
	[City] [varchar](100) NULL,
	[State] [varchar](2) NULL,
	[Population] [bigint] NULL,
	[Total] [int] NULL,
	[Total1000] [float] NULL,
 CONSTRAINT [PK_CrimeRate] PRIMARY KEY CLUSTERED 
	(
		[CrimeRateID] ASC
	)
) ON [PRIMARY]
GO

CREATE TABLE [dbo].[FFL](
	[FFLID] [int] IDENTITY(1,1) NOT NULL,
	[Name] [varchar](100) NULL,
	[Address] [varchar](100) NULL,
	[City] [varchar](100) NULL,
	[State] [varchar](2) NULL,
	[Zip] [varchar](20) NULL,
	[Lat] [float] NULL,
	[Lng] [float] NULL,
 CONSTRAINT [PK_FFL] PRIMARY KEY CLUSTERED 
	(
		[FFLID] ASC
	)
) ON [PRIMARY]
GO

CREATE TABLE [dbo].[PoliceStation](
	[StationID] [int] IDENTITY(1,1) NOT NULL,
	[URL] [varchar](200) NULL,
	[Name] [varchar](100) NULL,
	[Address1] [varchar](100) NULL,
	[Address2] [varchar](100) NULL,
	[City] [varchar](100) NULL,
	[State] [varchar](2) NULL,
	[Zip] [varchar](20) NULL,
	[Population] [int] NULL,
	[Officers] [int] NULL,
	[Lat] [float] NULL,
	[Lng] [float] NULL,
 CONSTRAINT [PK_PoliceStation] PRIMARY KEY CLUSTERED 
	(
		[StationID] ASC
	)
) ON [PRIMARY]
GO

CREATE TABLE [dbo].[Rating](
	[ReviewID] [int] IDENTITY(1,1) NOT NULL,
	[BankID] [int] NOT NULL,
	[Rating] [int] NULL,
	[Text] [varchar](max) NULL,
	[Author_Name] [varchar](100) NULL,
	[Author_Url] [varchar](2048) NULL,
 CONSTRAINT [PK_Rating] PRIMARY KEY CLUSTERED 
	(
		[ReviewID] ASC
	)
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

CREATE TABLE [dbo].[Review](
	[ReviewID] [int] IDENTITY(1,1) NOT NULL,
	[BankID] [int] NOT NULL,
	[Rating] [int] NULL,
	[Text] [varchar](max) NULL,
	[Author_Name] [varchar](100) NULL,
	[Author_Url] [varchar](2048) NULL,
 CONSTRAINT [PK_Review] PRIMARY KEY CLUSTERED 
	(
		[ReviewID] ASC
	)
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

ALTER TABLE [dbo].[Review]  WITH CHECK ADD  CONSTRAINT [FK_Bank_Review] FOREIGN KEY([BankID])
REFERENCES [dbo].[Bank] ([BankID])
ON DELETE CASCADE
GO

ALTER TABLE [dbo].[Review] CHECK CONSTRAINT [FK_Bank_Review]
GO

CREATE VIEW [dbo].[BankSampleView]
AS
SELECT        b.BankID, b.UniqueNum, b.Name, b.Address1, b.Address2, b.City, b.State, b.Zip, b.Deposit, b.Lat, b.Lng, b.ClosestStationID, b.ClosestPSDistance, b.MeanPSDistance, b.PSCount, b.Take, b.PDistance, b.Officers1000, b.FFLCount, 
                         b.AvgRating, b.Target, cr.Population, cr.Total1000 AS CrimeRate1000
FROM            dbo.BankSample AS b LEFT OUTER JOIN
                         dbo.CrimeRate AS cr ON cr.City = b.City AND cr.State = b.State
GO

CREATE VIEW [dbo].[BankView]
AS
SELECT        b.BankID, b.UniqueNum, b.Name, b.Address1, b.Address2, b.City, b.State, b.Zip, b.Deposit, b.Lat, b.Lng, b.ClosestStationID, b.ClosestPSDistance, b.MeanPSDistance, b.PSCount, b.Take, b.PDistance, b.Officers1000, b.FFLCount, 
                         b.AvgRating, b.Target, cr.Population, cr.Total1000 AS CrimeRate1000
FROM            dbo.Bank AS b LEFT OUTER JOIN
                         dbo.CrimeRate AS cr ON cr.City = b.City AND cr.State = b.State
GO
