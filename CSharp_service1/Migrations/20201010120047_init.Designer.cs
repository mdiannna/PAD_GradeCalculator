﻿// <auto-generated />
using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Metadata;
using Microsoft.EntityFrameworkCore.Migrations;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;
using UserMicroservice;

namespace UserMicroservice.Migrations
{
    [DbContext(typeof(UniversityContext))]
    [Migration("20201010120047_init")]
    partial class init
    {
        protected override void BuildTargetModel(ModelBuilder modelBuilder)
        {
#pragma warning disable 612, 618
            modelBuilder
                .HasAnnotation("ProductVersion", "2.2.6-servicing-10079")
                .HasAnnotation("Relational:MaxIdentifierLength", 128)
                .HasAnnotation("SqlServer:ValueGenerationStrategy", SqlServerValueGenerationStrategy.IdentityColumn);

            modelBuilder.Entity("UserMicroservice.Models.Mark", b =>
                {
                    b.Property<int>("ID")
                        .ValueGeneratedOnAdd()
                        .HasAnnotation("SqlServer:ValueGenerationStrategy", SqlServerValueGenerationStrategy.IdentityColumn);

                    b.Property<int>("AtestationNo");

                    b.Property<int?>("StudentID");

                    b.Property<string>("Type");

                    b.Property<int>("Value");

                    b.HasKey("ID");

                    b.HasIndex("StudentID");

                    b.ToTable("Marks");
                });

            modelBuilder.Entity("UserMicroservice.Models.Student", b =>
                {
                    b.Property<int>("ID")
                        .ValueGeneratedOnAdd()
                        .HasAnnotation("SqlServer:ValueGenerationStrategy", SqlServerValueGenerationStrategy.IdentityColumn);

                    b.Property<string>("Group");

                    b.Property<string>("Name");

                    b.HasKey("ID");

                    b.ToTable("Students");
                });

            modelBuilder.Entity("UserMicroservice.Models.Mark", b =>
                {
                    b.HasOne("UserMicroservice.Models.Student", "Student")
                        .WithMany()
                        .HasForeignKey("StudentID");
                });
#pragma warning restore 612, 618
        }
    }
}
