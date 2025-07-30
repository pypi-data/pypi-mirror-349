# Datový model Registru osob SYSNET

Projekt obsahuje knihovnu Python s kompletním datovým modelem Registru osob SYSNET

## Verze 1

V této verzi jsou implementovány tyto třídy: 

### common

Třídy pro obecné použití rozšířené pro Registr osob

1. ContactType
2. DepartmentType 
3. IssuingType 
4. MembershipEnum 
5. MemberType 
6. RedundantType 
7. RegistryEnum 
8. RegistryType


### config

Konfigurace služby (rozpracováno)

1. ConfigType


### context

Uživatelský kontext

1. ContextIndividualType  
2. ContextPersonsType 
3. ContextRolesType


### individual

Uživatelé

1. IndividualBaseType 
2. IndividualEntryType 
3. IndividualListType 
4. IndividualType

### person

Subjekty

1. PersonBaseType
2. PersonEntryType
3. PersonLinkType
4. PersonListType
5. PersonType

### role

Role

1. RoleBaseType
2. RoleCategoryEnum
3. RoleCategoryType
4. RoleEntryType
5. RoleListType
6. RoleType

### tag

Tagy

1. TagItemType
2. TagListType
3. TagType
