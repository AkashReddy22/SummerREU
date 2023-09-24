CREATE VIEW BigTable AS
SELECT person_agg.*, 
o_add.AddressLine AS "PERM_AddressLine",
o_add.City AS "PERM_City",
o_add.State AS "PERM_State",
o_add.ZipCode AS "PERM_ZipCode",
o_add.CountryName AS "PERM_CountryName",
o_add.Phone AS "PERM_Phone",
o_add.Fax AS "PERM_Fax",
c_add.AddressLine AS "CUR_AddressLine",
c_add.City AS "CUR_City",
c_add.State AS "CUR_State",
c_add.ZipCode AS "CUR_ZipCode",
c_add.CountryName AS "CUR_CountryName",
c_add.Phone AS "CUR_Phone",
c_add.Fax AS "CUR_Fax",
grad.InstituteName AS "GradInstituteName",
grad.DegreeReceived AS "GradDegreeReceived",
grad.DegreePlanned AS "GradDegreePlanned",
grad.Program AS "GradProgram",
grad.Major AS "GradMajor",
ug.InstituteName AS "UnderGradInstituteName",
ug.Degree AS "UnderGradDegree",
ug.Major AS "UnderGradMajor"
FROM 
    (SELECT *
    FROM  Person p 
    LEFT JOIN Ethinic e ON p.EthinicityID=e.EthinicID 
    LEFT JOIN MtbiInfo m USING (PersonID)
    LEFT JOIN Gender g USING (GenderID) 
    LEFT JOIN Publications pub USING (PersonID)) person_agg
LEFT JOIN Address o_add ON person_agg.PermanentAddressID=o_add.AddressID
LEFT JOIN Address c_add ON person_agg.CurrentAddressID=c_add.AddressID
LEFT JOIN Grad grad USING (PersonID)
LEFT JOIN UnderGrad ug USING (PersonID);