"""
    @file: orm/files.py
    @author: Suraj Kumar Giri (@surajgirioffl)
    @init-date: 11th Feb 2024
    @last-modified: 11th Feb 2024
    
    Description:
        * Module containing Models associated with the database 'files'.
"""

from sqlalchemy import create_engine, Column, Integer, String, Enum, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Files(Base):
    __tablename__ = "files"
    SNo = Column(Integer, nullable=False, unique=True, autoincrement=True)
    FileId = Column(Integer, primary_key=True)
    Title = Column(String(255), nullable=False)
    Access = Column(Enum("Public", "Private", "Restricted"), nullable=False, default="Public")
    ServeVia = Column(Enum("FileSystem", "Drive"), nullable=False, default="Drive")


class FilesPath(Base):
    __tablename__ = "files_path"
    SNo = Column(Integer, nullable=False, unique=True, autoincrement=True)
    FileId = Column(Integer, ForeignKey("files.FileId"), primary_key=True)
    FilePath = Column(String(400), unique=True, nullable=False)


class Drive(Base):
    __tablename__ = "drive"
    SNo = Column(Integer, nullable=False, unique=True, autoincrement=True)
    FileId = Column(Integer, ForeignKey("files.FileId"), primary_key=True)
    ViewLink = Column(String(200), unique=True, nullable=False)
    DownloadLink = Column(String(200), unique=True, nullable=False)


class FileContentsInfo(Base):
    __tablename__ = "file_contents_info"
    SNo = Column(Integer, nullable=False, unique=True, autoincrement=True)
    FileId = Column(Integer, ForeignKey("files.FileId"), primary_key=True)
    Description = Column(String(600), nullable=False)
    Keywords = Column(String(500), nullable=False)


class FilesType(Base):
    __tablename__ = "files_type"
    SNo = Column(Integer, nullable=False, unique=True, autoincrement=True)
    Extension = Column(String(10), primary_key=True)
    FileType = Column(String(30), nullable=False)


class FilesMetadata(Base):
    __tablename__ = "files_metadata"
    SNo = Column(Integer, nullable=False, unique=True, autoincrement=True)
    FileId = Column(Integer, ForeignKey("files.FileId"), primary_key=True)
    FileName = Column(String(100), nullable=False)
    DownloadName = Column(String(100), nullable=False)
    Extension = Column(String(10), ForeignKey("files_type.Extension"), nullable=False)
    Size = Column(Float, nullable=False)


class FilesInfo(Base):
    __tablename__ = "files_info"
    SNo = Column(Integer, nullable=False, unique=True, autoincrement=True)
    FileId = Column(Integer, ForeignKey("files.FileId"), primary_key=True)
    Category = Column(String(50), nullable=False)
    FileFor = Column(String(50), nullable=False)
    DateCreated = Column(DateTime, nullable=False, default=datetime.utcnow)
    DateModified = Column(DateTime, nullable=False, default=datetime.utcnow)
    Tags = Column(String(200), nullable=False)


class FilesTracking(Base):
    __tablename__ = "files_tracking"
    SNo = Column(Integer, nullable=False, unique=True, autoincrement=True)
    FileId = Column(Integer, ForeignKey("files.FileId"), primary_key=True)
    DownloadCount = Column(Integer, nullable=False, default=0)
    LastDownloaded = Column(DateTime, nullable=False, default=datetime.utcnow)


class FilesViewsTracking(Base):
    __tablename__ = "files_views_tracking"
    SNo = Column(Integer, nullable=False, unique=True, autoincrement=True)
    FileId = Column(Integer, ForeignKey("files.FileId"), primary_key=True)
    ViewsCount = Column(Integer, nullable=False, default=0)
    LastViewed = Column(DateTime, nullable=False, default=datetime.utcnow)


class CreditorsInfo(Base):
    __tablename__ = "creditors_info"
    SNo = Column(Integer, nullable=False, unique=True, autoincrement=True)
    Id = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False)
    Email = Column(String(100), unique=True, nullable=False)
    Designation = Column(String(50), default=None)
    Username = Column(String(50), unique=True, default=None)
    AccountId = Column(Integer, unique=True, default=None)
    Contact = Column(String(100), unique=True, default=None)


class RootSources(Base):
    __tablename__ = "root_sources"
    SNo = Column(Integer, nullable=False, unique=True, autoincrement=True)
    Id = Column(Integer, primary_key=True)
    Name = Column(String(100), unique=True, nullable=False)
    ContactLink = Column(String(100), nullable=False)


class Credits(Base):
    __tablename__ = "credits"
    SNo = Column(Integer, nullable=False, unique=True, autoincrement=True)
    FileId = Column(Integer, ForeignKey("files.FileId"), primary_key=True)
    SubmitterId = Column(Integer, ForeignKey("creditors_info.Id"), nullable=False)
    SubmittedOn = Column(DateTime, nullable=False, default=datetime.utcnow)
    UploaderId = Column(Integer, ForeignKey("creditors_info.Id"), nullable=False)
    UploadedOn = Column(DateTime, nullable=False, default=datetime.utcnow)
    ModifierId = Column(Integer, ForeignKey("creditors_info.Id"), nullable=False)
    LastModifiedOn = Column(DateTime, nullable=False, default=datetime.utcnow)
    ApproverId = Column(Integer, ForeignKey("creditors_info.Id"), nullable=False)
    ApprovedOn = Column(DateTime, nullable=False, default=datetime.utcnow)
    RootSourceFileLink = Column(String(200), default=None)
    RootSourceId = Column(Integer, ForeignKey("root_sources.Id"), nullable=False)


# engine = create_engine("mysql://username:password@localhost/files")
# Base.metadata.create_all(engine)
