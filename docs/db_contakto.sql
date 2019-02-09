-- MySQL dump 10.13  Distrib 5.7.24, for Linux (x86_64)
--
-- Host: 9a8c04d547b2    Database: db_contakto
-- ------------------------------------------------------
-- Server version	5.7.24

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `adjuntos_adjuntos`
--

DROP TABLE IF EXISTS `adjuntos_adjuntos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adjuntos_adjuntos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `investigacion_id` int(11) NOT NULL,
  `adj1` varchar(100) DEFAULT NULL,
  `adj2` varchar(100) DEFAULT NULL,
  `adj3` varchar(100) DEFAULT NULL,
  `adj4` varchar(100) DEFAULT NULL,
  `adj5` varchar(100) DEFAULT NULL,
  `adj6` varchar(100) DEFAULT NULL,
  `adj7` varchar(100) DEFAULT NULL,
  `adj8` varchar(100) DEFAULT NULL,
  `adj9` varchar(100) DEFAULT NULL,
  `adj10` varchar(100) DEFAULT NULL,
  `adj11` varchar(100) DEFAULT NULL,
  `adj12` varchar(100) DEFAULT NULL,
  `adj13` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `adjuntos_adjuntos_e5ec9382` (`investigacion_id`),
  CONSTRAINT `investigacion_id_refs_id_ad0fe8a1` FOREIGN KEY (`investigacion_id`) REFERENCES `investigacion_investigacion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adjuntos_adjuntos`
--

LOCK TABLES `adjuntos_adjuntos` WRITE;
/*!40000 ALTER TABLE `adjuntos_adjuntos` DISABLE KEYS */;
INSERT INTO `adjuntos_adjuntos` VALUES (1,4,'','adj/WhatsApp_Image_2019-01-21_at_08.16.40.jpeg','','','','','','','','','','',''),(2,5,'adj/RFC_CONTAKTO.pdf','','','','','','','','','','','','');
/*!40000 ALTER TABLE `adjuntos_adjuntos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `agente_agenteinfo`
--

DROP TABLE IF EXISTS `agente_agenteinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `agente_agenteinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `agente_id` int(11) NOT NULL,
  `telefono` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `agente_agenteinfo_730b2c6a` (`agente_id`),
  CONSTRAINT `agente_id_refs_id_2cade46e` FOREIGN KEY (`agente_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `agente_agenteinfo`
--

LOCK TABLES `agente_agenteinfo` WRITE;
/*!40000 ALTER TABLE `agente_agenteinfo` DISABLE KEYS */;
INSERT INTO `agente_agenteinfo` VALUES (1,1,''),(2,2,''),(3,4,'');
/*!40000 ALTER TABLE `agente_agenteinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_bda51c3c` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_a7792de1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_e4470c6e` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=253 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add site',6,'add_site'),(17,'Can change site',6,'change_site'),(18,'Can delete site',6,'delete_site'),(19,'Can add migration history',7,'add_migrationhistory'),(20,'Can change migration history',7,'change_migrationhistory'),(21,'Can delete migration history',7,'delete_migrationhistory'),(22,'Can add log entry',8,'add_logentry'),(23,'Can change log entry',8,'change_logentry'),(24,'Can delete log entry',8,'delete_logentry'),(25,'Can add agente info',9,'add_agenteinfo'),(26,'Can change agente info',9,'change_agenteinfo'),(27,'Can delete agente info',9,'delete_agenteinfo'),(28,'Can add bitacora',10,'add_bitacora'),(29,'Can change bitacora',10,'change_bitacora'),(30,'Can delete bitacora',10,'delete_bitacora'),(31,'Can add Compañia',11,'add_compania'),(32,'Can change Compañia',11,'change_compania'),(33,'Can delete Compañia',11,'delete_compania'),(34,'Can add Contacto',12,'add_contacto'),(35,'Can change Contacto',12,'change_contacto'),(36,'Can delete Contacto',12,'delete_contacto'),(37,'Can add investigacion',13,'add_investigacion'),(38,'Can change investigacion',13,'change_investigacion'),(39,'Can delete investigacion',13,'delete_investigacion'),(40,'Can add file',14,'add_file'),(41,'Can change file',14,'change_file'),(42,'Can delete file',14,'delete_file'),(43,'Can add persona',15,'add_persona'),(44,'Can change persona',15,'change_persona'),(45,'Can delete persona',15,'delete_persona'),(46,'Can add telefono',16,'add_telefono'),(47,'Can change telefono',16,'change_telefono'),(48,'Can delete telefono',16,'delete_telefono'),(49,'Can add direccion',17,'add_direccion'),(50,'Can change direccion',17,'change_direccion'),(51,'Can delete direccion',17,'delete_direccion'),(52,'Can add prestacion vivienda',18,'add_prestacionvivienda'),(53,'Can change prestacion vivienda',18,'change_prestacionvivienda'),(54,'Can delete prestacion vivienda',18,'delete_prestacionvivienda'),(55,'Can add licencia',19,'add_licencia'),(56,'Can change licencia',19,'change_licencia'),(57,'Can delete licencia',19,'delete_licencia'),(58,'Can add origen',20,'add_origen'),(59,'Can change origen',20,'change_origen'),(60,'Can delete origen',20,'delete_origen'),(61,'Can add info personal',21,'add_infopersonal'),(62,'Can change info personal',21,'change_infopersonal'),(63,'Can delete info personal',21,'delete_infopersonal'),(64,'Can add trayectoria laboral',22,'add_trayectorialaboral'),(65,'Can change trayectoria laboral',22,'change_trayectorialaboral'),(66,'Can delete trayectoria laboral',22,'delete_trayectorialaboral'),(67,'Can add legalidad',23,'add_legalidad'),(68,'Can change legalidad',23,'change_legalidad'),(69,'Can delete legalidad',23,'delete_legalidad'),(70,'Can add seguro',24,'add_seguro'),(71,'Can change seguro',24,'change_seguro'),(72,'Can delete seguro',24,'delete_seguro'),(73,'Can add salud',25,'add_salud'),(74,'Can change salud',25,'change_salud'),(75,'Can delete salud',25,'delete_salud'),(76,'Can add actividades habitos',26,'add_actividadeshabitos'),(77,'Can change actividades habitos',26,'change_actividadeshabitos'),(78,'Can delete actividades habitos',26,'delete_actividadeshabitos'),(79,'Can add academica',27,'add_academica'),(80,'Can change academica',27,'change_academica'),(81,'Can delete academica',27,'delete_academica'),(82,'Can add grado escolaridad',28,'add_gradoescolaridad'),(83,'Can change grado escolaridad',28,'change_gradoescolaridad'),(84,'Can delete grado escolaridad',28,'delete_gradoescolaridad'),(85,'Can add otro idioma',29,'add_otroidioma'),(86,'Can change otro idioma',29,'change_otroidioma'),(87,'Can delete otro idioma',29,'delete_otroidioma'),(88,'Can add situacion vivienda',30,'add_situacionvivienda'),(89,'Can change situacion vivienda',30,'change_situacionvivienda'),(90,'Can delete situacion vivienda',30,'delete_situacionvivienda'),(91,'Can add propietario vivienda',31,'add_propietariovivienda'),(92,'Can change propietario vivienda',31,'change_propietariovivienda'),(93,'Can delete propietario vivienda',31,'delete_propietariovivienda'),(94,'Can add caractaristicas vivienda',32,'add_caractaristicasvivienda'),(95,'Can change caractaristicas vivienda',32,'change_caractaristicasvivienda'),(96,'Can delete caractaristicas vivienda',32,'delete_caractaristicasvivienda'),(97,'Can add tipo inmueble',33,'add_tipoinmueble'),(98,'Can change tipo inmueble',33,'change_tipoinmueble'),(99,'Can delete tipo inmueble',33,'delete_tipoinmueble'),(100,'Can add distribucion dimensiones',34,'add_distribuciondimensiones'),(101,'Can change distribucion dimensiones',34,'change_distribuciondimensiones'),(102,'Can delete distribucion dimensiones',34,'delete_distribuciondimensiones'),(103,'Can add miembro marco familiar',35,'add_miembromarcofamiliar'),(104,'Can change miembro marco familiar',35,'change_miembromarcofamiliar'),(105,'Can delete miembro marco familiar',35,'delete_miembromarcofamiliar'),(106,'Can add economica',36,'add_economica'),(107,'Can change economica',36,'change_economica'),(108,'Can delete economica',36,'delete_economica'),(109,'Can add tarjeta credito comercial',37,'add_tarjetacreditocomercial'),(110,'Can change tarjeta credito comercial',37,'change_tarjetacreditocomercial'),(111,'Can delete tarjeta credito comercial',37,'delete_tarjetacreditocomercial'),(112,'Can add cuenta debito',38,'add_cuentadebito'),(113,'Can change cuenta debito',38,'change_cuentadebito'),(114,'Can delete cuenta debito',38,'delete_cuentadebito'),(115,'Can add automovil',39,'add_automovil'),(116,'Can change automovil',39,'change_automovil'),(117,'Can delete automovil',39,'delete_automovil'),(118,'Can add bienes raices',40,'add_bienesraices'),(119,'Can change bienes raices',40,'change_bienesraices'),(120,'Can delete bienes raices',40,'delete_bienesraices'),(121,'Can add deuda actual',41,'add_deudaactual'),(122,'Can change deuda actual',41,'change_deudaactual'),(123,'Can delete deuda actual',41,'delete_deudaactual'),(124,'Can add referencia',42,'add_referencia'),(125,'Can change referencia',42,'change_referencia'),(126,'Can delete referencia',42,'delete_referencia'),(127,'Can add cuadro evaluacion',43,'add_cuadroevaluacion'),(128,'Can change cuadro evaluacion',43,'change_cuadroevaluacion'),(129,'Can delete cuadro evaluacion',43,'delete_cuadroevaluacion'),(130,'Can add documento cotejado',44,'add_documentocotejado'),(131,'Can change documento cotejado',44,'change_documentocotejado'),(132,'Can delete documento cotejado',44,'delete_documentocotejado'),(133,'Can add aspecto hogar',45,'add_aspectohogar'),(134,'Can change aspecto hogar',45,'change_aspectohogar'),(135,'Can delete aspecto hogar',45,'delete_aspectohogar'),(136,'Can add aspecto candidato',46,'add_aspectocandidato'),(137,'Can change aspecto candidato',46,'change_aspectocandidato'),(138,'Can delete aspecto candidato',46,'delete_aspectocandidato'),(139,'Can add evaluacion',47,'add_evaluacion'),(140,'Can change evaluacion',47,'change_evaluacion'),(141,'Can delete evaluacion',47,'delete_evaluacion'),(142,'Can add opinion',48,'add_opinion'),(143,'Can change opinion',48,'change_opinion'),(144,'Can delete opinion',48,'delete_opinion'),(145,'Can add informante',49,'add_informante'),(146,'Can change informante',49,'change_informante'),(147,'Can delete informante',49,'delete_informante'),(148,'Can add entrevista file',50,'add_entrevistafile'),(149,'Can change entrevista file',50,'change_entrevistafile'),(150,'Can delete entrevista file',50,'delete_entrevistafile'),(151,'Can add entrevista persona',51,'add_entrevistapersona'),(152,'Can change entrevista persona',51,'change_entrevistapersona'),(153,'Can delete entrevista persona',51,'delete_entrevistapersona'),(154,'Can add entrevista investigacion',52,'add_entrevistainvestigacion'),(155,'Can change entrevista investigacion',52,'change_entrevistainvestigacion'),(156,'Can delete entrevista investigacion',52,'delete_entrevistainvestigacion'),(157,'Can add entrevista cita',53,'add_entrevistacita'),(158,'Can change entrevista cita',53,'change_entrevistacita'),(159,'Can delete entrevista cita',53,'delete_entrevistacita'),(160,'Can add entrevista telefono',54,'add_entrevistatelefono'),(161,'Can change entrevista telefono',54,'change_entrevistatelefono'),(162,'Can delete entrevista telefono',54,'delete_entrevistatelefono'),(163,'Can add entrevista direccion',55,'add_entrevistadireccion'),(164,'Can change entrevista direccion',55,'change_entrevistadireccion'),(165,'Can delete entrevista direccion',55,'delete_entrevistadireccion'),(166,'Can add entrevista prestacion vivienda',56,'add_entrevistaprestacionvivienda'),(167,'Can change entrevista prestacion vivienda',56,'change_entrevistaprestacionvivienda'),(168,'Can delete entrevista prestacion vivienda',56,'delete_entrevistaprestacionvivienda'),(169,'Can add entrevista licencia',57,'add_entrevistalicencia'),(170,'Can change entrevista licencia',57,'change_entrevistalicencia'),(171,'Can delete entrevista licencia',57,'delete_entrevistalicencia'),(172,'Can add entrevista origen',58,'add_entrevistaorigen'),(173,'Can change entrevista origen',58,'change_entrevistaorigen'),(174,'Can delete entrevista origen',58,'delete_entrevistaorigen'),(175,'Can add entrevista info personal',59,'add_entrevistainfopersonal'),(176,'Can change entrevista info personal',59,'change_entrevistainfopersonal'),(177,'Can delete entrevista info personal',59,'delete_entrevistainfopersonal'),(178,'Can add entrevista historial en empresa',60,'add_entrevistahistorialenempresa'),(179,'Can change entrevista historial en empresa',60,'change_entrevistahistorialenempresa'),(180,'Can delete entrevista historial en empresa',60,'delete_entrevistahistorialenempresa'),(181,'Can add entrevista salud',61,'add_entrevistasalud'),(182,'Can change entrevista salud',61,'change_entrevistasalud'),(183,'Can delete entrevista salud',61,'delete_entrevistasalud'),(184,'Can add entrevista actividades habitos',62,'add_entrevistaactividadeshabitos'),(185,'Can change entrevista actividades habitos',62,'change_entrevistaactividadeshabitos'),(186,'Can delete entrevista actividades habitos',62,'delete_entrevistaactividadeshabitos'),(187,'Can add entrevista academica',63,'add_entrevistaacademica'),(188,'Can change entrevista academica',63,'change_entrevistaacademica'),(189,'Can delete entrevista academica',63,'delete_entrevistaacademica'),(190,'Can add entrevista grado escolaridad',64,'add_entrevistagradoescolaridad'),(191,'Can change entrevista grado escolaridad',64,'change_entrevistagradoescolaridad'),(192,'Can delete entrevista grado escolaridad',64,'delete_entrevistagradoescolaridad'),(193,'Can add entrevista otro idioma',65,'add_entrevistaotroidioma'),(194,'Can change entrevista otro idioma',65,'change_entrevistaotroidioma'),(195,'Can delete entrevista otro idioma',65,'delete_entrevistaotroidioma'),(196,'Can add entrevista situacion vivienda',66,'add_entrevistasituacionvivienda'),(197,'Can change entrevista situacion vivienda',66,'change_entrevistasituacionvivienda'),(198,'Can delete entrevista situacion vivienda',66,'delete_entrevistasituacionvivienda'),(199,'Can add entrevista propietario vivienda',67,'add_entrevistapropietariovivienda'),(200,'Can change entrevista propietario vivienda',67,'change_entrevistapropietariovivienda'),(201,'Can delete entrevista propietario vivienda',67,'delete_entrevistapropietariovivienda'),(202,'Can add entrevista caractaristicas vivienda',68,'add_entrevistacaractaristicasvivienda'),(203,'Can change entrevista caractaristicas vivienda',68,'change_entrevistacaractaristicasvivienda'),(204,'Can delete entrevista caractaristicas vivienda',68,'delete_entrevistacaractaristicasvivienda'),(205,'Can add entrevista tipo inmueble',69,'add_entrevistatipoinmueble'),(206,'Can change entrevista tipo inmueble',69,'change_entrevistatipoinmueble'),(207,'Can delete entrevista tipo inmueble',69,'delete_entrevistatipoinmueble'),(208,'Can add entrevista distribucion dimensiones',70,'add_entrevistadistribuciondimensiones'),(209,'Can change entrevista distribucion dimensiones',70,'change_entrevistadistribuciondimensiones'),(210,'Can delete entrevista distribucion dimensiones',70,'delete_entrevistadistribuciondimensiones'),(211,'Can add entrevista miembro marco familiar',71,'add_entrevistamiembromarcofamiliar'),(212,'Can change entrevista miembro marco familiar',71,'change_entrevistamiembromarcofamiliar'),(213,'Can delete entrevista miembro marco familiar',71,'delete_entrevistamiembromarcofamiliar'),(214,'Can add entrevista economica',72,'add_entrevistaeconomica'),(215,'Can change entrevista economica',72,'change_entrevistaeconomica'),(216,'Can delete entrevista economica',72,'delete_entrevistaeconomica'),(217,'Can add entrevista tarjeta credito comercial',73,'add_entrevistatarjetacreditocomercial'),(218,'Can change entrevista tarjeta credito comercial',73,'change_entrevistatarjetacreditocomercial'),(219,'Can delete entrevista tarjeta credito comercial',73,'delete_entrevistatarjetacreditocomercial'),(220,'Can add entrevista cuenta debito',74,'add_entrevistacuentadebito'),(221,'Can change entrevista cuenta debito',74,'change_entrevistacuentadebito'),(222,'Can delete entrevista cuenta debito',74,'delete_entrevistacuentadebito'),(223,'Can add entrevista automovil',75,'add_entrevistaautomovil'),(224,'Can change entrevista automovil',75,'change_entrevistaautomovil'),(225,'Can delete entrevista automovil',75,'delete_entrevistaautomovil'),(226,'Can add entrevista bienes raices',76,'add_entrevistabienesraices'),(227,'Can change entrevista bienes raices',76,'change_entrevistabienesraices'),(228,'Can delete entrevista bienes raices',76,'delete_entrevistabienesraices'),(229,'Can add entrevista seguro',77,'add_entrevistaseguro'),(230,'Can change entrevista seguro',77,'change_entrevistaseguro'),(231,'Can delete entrevista seguro',77,'delete_entrevistaseguro'),(232,'Can add entrevista deuda actual',78,'add_entrevistadeudaactual'),(233,'Can change entrevista deuda actual',78,'change_entrevistadeudaactual'),(234,'Can delete entrevista deuda actual',78,'delete_entrevistadeudaactual'),(235,'Can add entrevista referencia',79,'add_entrevistareferencia'),(236,'Can change entrevista referencia',79,'change_entrevistareferencia'),(237,'Can delete entrevista referencia',79,'delete_entrevistareferencia'),(238,'Can add entrevista documento cotejado',80,'add_entrevistadocumentocotejado'),(239,'Can change entrevista documento cotejado',80,'change_entrevistadocumentocotejado'),(240,'Can delete entrevista documento cotejado',80,'delete_entrevistadocumentocotejado'),(241,'Can add entrevista aspecto hogar',81,'add_entrevistaaspectohogar'),(242,'Can change entrevista aspecto hogar',81,'change_entrevistaaspectohogar'),(243,'Can delete entrevista aspecto hogar',81,'delete_entrevistaaspectohogar'),(244,'Can add entrevista aspecto candidato',82,'add_entrevistaaspectocandidato'),(245,'Can change entrevista aspecto candidato',82,'change_entrevistaaspectocandidato'),(246,'Can delete entrevista aspecto candidato',82,'delete_entrevistaaspectocandidato'),(247,'Can add cobranza',83,'add_cobranza'),(248,'Can change cobranza',83,'change_cobranza'),(249,'Can delete cobranza',83,'delete_cobranza'),(250,'Can add adjuntos',84,'add_adjuntos'),(251,'Can change adjuntos',84,'change_adjuntos'),(252,'Can delete adjuntos',84,'delete_adjuntos');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'admint','a','a','info@mintitmedia.com','pbkdf2_sha256$10000$0iVlRHZJNP6o$Sby4on3IKXJ0RC+JmblcqSapPPkM2a4/1nSQsSrGjBw=',1,1,1,'2019-02-06 01:02:55','2019-01-18 23:20:30'),(2,'contakto','','','contaktouno@hotmail.com','pbkdf2_sha256$10000$OzXgZeuSCBKV$XGa6w8j/I8ZGDRT4O/SntBTRmhKiLq+/dbjpyNSsg1o=',1,1,1,'2019-02-06 22:21:21','2019-01-18 23:23:43'),(3,'','','','fernanda@contakto.mx','pbkdf2_sha256$10000$fw8svvv7dSsh$2OkgraNreaAKXQFpRKS9xmCfsOylLGGoGs4pUQyhHNg=',0,1,0,'2019-01-24 01:35:08','2019-01-24 01:35:08'),(4,'Mariana','Mariana','vc','irene@contakto.mx','pbkdf2_sha256$10000$lmvurzbVd12s$eG6/QxG6Zz+aGimK8qGxrHdo+UHg1pV8UjdZ7wChVcg=',1,1,0,'2019-02-06 01:03:22','2019-01-24 02:06:32');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_fbfc09f1` (`user_id`),
  KEY `auth_user_groups_bda51c3c` (`group_id`),
  CONSTRAINT `group_id_refs_id_f0ee9890` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_831107f1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_fbfc09f1` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_f2045483` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bitacora_bitacora`
--

DROP TABLE IF EXISTS `bitacora_bitacora`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bitacora_bitacora` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action` varchar(120) NOT NULL,
  `user_id` int(11) NOT NULL,
  `datetime` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `bitacora_bitacora_fbfc09f1` (`user_id`),
  CONSTRAINT `user_id_refs_id_90b6d5e8` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=156 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bitacora_bitacora`
--

LOCK TABLES `bitacora_bitacora` WRITE;
/*!40000 ALTER TABLE `bitacora_bitacora` DISABLE KEYS */;
INSERT INTO `bitacora_bitacora` VALUES (1,'login',1,'2019-01-18 23:21:54'),(2,'logout',1,'2019-01-18 23:23:50'),(3,'login',2,'2019-01-18 23:23:55'),(4,'logout',2,'2019-01-18 23:23:57'),(5,'login',2,'2019-01-18 23:36:58'),(6,'login',1,'2019-01-21 18:36:04'),(7,'login',2,'2019-01-24 01:29:06'),(8,'login',2,'2019-01-24 01:30:19'),(9,'empresas-creada: None',2,'2019-01-24 01:33:46'),(10,'candidato-creado: Fernanda',2,'2019-01-24 01:36:12'),(11,'candidato-creado: Fernanda',2,'2019-01-24 01:39:54'),(12,'candidato-editado: Fernanda',2,'2019-01-24 01:40:24'),(13,'trayectoria-nueva: Fernanda/ABC',2,'2019-01-24 01:42:25'),(14,'trayectoria-editar: Fernanda/ABC',2,'2019-01-24 01:44:34'),(15,'trayectoria-editar: Fernanda/ABC',2,'2019-01-24 01:45:09'),(16,'investigacion-eliminada: Fernanda / ABC',2,'2019-01-24 01:46:30'),(17,'contacto-editado: Fernanda Angulo / ABC',2,'2019-01-24 01:50:11'),(18,'logout',2,'2019-01-24 01:50:14'),(19,'login',2,'2019-01-24 01:50:32'),(20,'contacto-editado: Fernanda Angulo / ABC',2,'2019-01-24 01:51:23'),(21,'logout',2,'2019-01-24 01:51:31'),(22,'login',2,'2019-01-24 01:51:47'),(23,'logout',2,'2019-01-24 01:53:01'),(24,'login',2,'2019-01-24 01:53:14'),(25,'contacto-editado: Fernanda Angulo / ABC',2,'2019-01-24 01:54:34'),(26,'contacto-editado: Fernanda Angulo / ABC',2,'2019-01-24 01:54:43'),(27,'logout',2,'2019-01-24 01:54:50'),(28,'login',2,'2019-01-24 01:55:10'),(29,'logout',2,'2019-01-24 01:55:23'),(30,'login',2,'2019-01-24 01:55:26'),(31,'contacto-editado: Fernanda Angulo / ABC',2,'2019-01-24 01:56:16'),(32,'logout',2,'2019-01-24 01:56:23'),(33,'logout',2,'2019-01-24 01:57:49'),(34,'login',2,'2019-01-24 01:57:51'),(35,'trayectoria-editar: Fernanda/ABC',2,'2019-01-24 01:59:46'),(36,'trayectoria-editar: Fernanda/ABC',2,'2019-01-24 02:00:30'),(37,'trayectoria-editar: Fernanda/ABC',2,'2019-01-24 02:01:39'),(38,'trayectoria-editar: Fernanda/ABC',2,'2019-01-24 02:03:07'),(39,'login',2,'2019-01-24 02:03:31'),(40,'logout',2,'2019-01-24 02:03:41'),(41,'login',2,'2019-01-24 02:03:42'),(42,'contacto-editado: Fernanda Angulo / ABC',2,'2019-01-24 02:04:11'),(43,'trayectoria-editar: Fernanda/ABC',2,'2019-01-24 02:04:23'),(44,'logout',2,'2019-01-24 02:04:32'),(45,'login',2,'2019-01-24 02:04:49'),(46,'logout',2,'2019-01-24 02:05:30'),(47,'crear-agente: Mariana',2,'2019-01-24 02:06:32'),(48,'logout',2,'2019-01-24 02:06:34'),(49,'login',4,'2019-01-24 02:06:38'),(50,'logout',4,'2019-01-24 02:06:47'),(51,'login',2,'2019-01-24 02:06:49'),(52,'candidato-editado: Fernanda',2,'2019-01-24 02:11:00'),(53,'logout',2,'2019-01-24 02:11:39'),(54,'login',2,'2019-01-24 02:11:40'),(55,'login',2,'2019-01-24 19:37:40'),(56,'login',2,'2019-01-24 19:39:53'),(57,'login',2,'2019-01-24 20:42:25'),(58,'login',2,'2019-01-25 16:53:53'),(59,'investigacion-eliminada: Fernanda / ABC',2,'2019-01-25 16:53:58'),(60,'borrar-empresa: ABC',2,'2019-01-25 16:54:07'),(61,'login',2,'2019-01-25 17:15:30'),(62,'empresas-creada: None',2,'2019-01-25 17:40:20'),(63,'empresas-creada: None',2,'2019-01-25 17:42:04'),(64,'borrar-contacto: SARA LOURDES MENDEZ BARRIOS (-) / GRUPO TRIMEX',2,'2019-01-25 17:52:14'),(65,'borrar-contacto: ALDAIR (-) / GRUPO TRIMEX',2,'2019-01-25 17:52:18'),(66,'borrar-contacto: Fernanda Angulo (-) / GRUPO TRIMEX',2,'2019-01-25 17:52:22'),(67,'borrar-contacto: SARA LOURDES MENDEZ BARRIOS (-) / GRUPO TRIMEX',2,'2019-01-25 17:52:26'),(68,'borrar-contacto: SARA LOURDES MENDEZ BARRIOS (-) / GRUPO TRIMEX',2,'2019-01-25 17:52:31'),(69,'borrar-contacto: SARA LOURDES MENDEZ BARRIOS (-) / GRUPO TRIMEX',2,'2019-01-25 17:52:36'),(70,'login',2,'2019-01-26 21:36:00'),(71,'candidato-creado: DOMINGO ANTONIO CASILLAS BARRAGAN',2,'2019-01-26 21:39:17'),(72,'trayectoria-nueva: DOMINGO ANTONIO CASILLAS BARRAGAN/VSH SEGURIDAD',2,'2019-01-26 21:39:33'),(73,'trayectoria-editar: DOMINGO ANTONIO CASILLAS BARRAGAN/VSH SEGURIDAD',2,'2019-01-26 21:43:17'),(74,'trayectoria-editar: DOMINGO ANTONIO CASILLAS BARRAGAN/VSH SEGURIDAD',2,'2019-01-26 21:47:51'),(75,'empresas-creada: None',2,'2019-01-26 21:50:46'),(76,'trayectoria-nueva: DOMINGO ANTONIO CASILLAS BARRAGAN/ALBATROS',2,'2019-01-26 21:51:04'),(77,'login',2,'2019-01-28 16:38:35'),(78,'login',2,'2019-01-29 15:43:33'),(79,'trayectoria-editar: DOMINGO ANTONIO CASILLAS BARRAGAN/ALBATROS',2,'2019-01-29 15:46:11'),(80,'empresas-creada: None',2,'2019-01-29 15:47:29'),(81,'trayectoria-nueva: DOMINGO ANTONIO CASILLAS BARRAGAN/HOTEL COLONIAL',2,'2019-01-29 15:47:34'),(82,'trayectoria-editar: DOMINGO ANTONIO CASILLAS BARRAGAN/HOTEL COLONIAL',2,'2019-01-29 15:49:37'),(83,'empresas-creada: None',2,'2019-01-29 15:50:39'),(84,'trayectoria-nueva: DOMINGO ANTONIO CASILLAS BARRAGAN/MAJOR DRILLING',2,'2019-01-29 15:50:41'),(85,'trayectoria-editar: DOMINGO ANTONIO CASILLAS BARRAGAN/MAJOR DRILLING',2,'2019-01-29 15:52:45'),(86,'trayectoria-editar: DOMINGO ANTONIO CASILLAS BARRAGAN/MAJOR DRILLING',2,'2019-01-29 15:53:34'),(87,'candidato-editado: DOMINGO ANTONIO CASILLAS BARRAGAN',2,'2019-01-29 15:56:52'),(88,'empresas-creada: None',2,'2019-01-29 16:05:06'),(89,'contacto-editado: MARIANA MARTINEZ / AGENCIA CONTAKTO',2,'2019-01-29 16:06:53'),(90,'contacto-editado: MARIANA MARTINEZ / AGENCIA CONTAKTO',2,'2019-01-29 16:07:01'),(91,'borrar-contacto: ALDAIR CORTES (-) / AGENCIA CONTAKTO',2,'2019-01-29 16:14:43'),(92,'login',2,'2019-01-29 16:17:26'),(93,'candidato-creado: ARAEL FERNANDA ANGULO ATONDO',2,'2019-01-29 16:28:50'),(94,'empresas-creada: None',2,'2019-01-29 16:30:10'),(95,'trayectoria-nueva: ARAEL FERNANDA ANGULO ATONDO/CITY CLUB',2,'2019-01-29 16:30:13'),(96,'trayectoria-editar: ARAEL FERNANDA ANGULO ATONDO/CITY CLUB',2,'2019-01-29 16:33:17'),(97,'empresas-creada: None',1,'2019-01-29 21:26:52'),(98,'borrar-empresa: test',1,'2019-01-29 21:27:58'),(99,'contacto-creado: test / AGENCIA CONTAKTO',1,'2019-01-29 21:28:49'),(100,'contacto-editado:   / AGENCIA CONTAKTO',1,'2019-01-29 21:29:25'),(101,'borrar-contacto:   (-) / AGENCIA CONTAKTO',1,'2019-01-29 21:29:36'),(102,'contacto-creado: test / AGENCIA CONTAKTO',1,'2019-01-29 21:30:48'),(103,'borrar-contacto: test (-) / AGENCIA CONTAKTO',1,'2019-01-29 21:31:15'),(104,'empresas-editada: None',1,'2019-01-30 21:42:44'),(105,'contacto-creado: Nombre prueba / AGENCIA CONTAKTO',1,'2019-01-31 19:46:16'),(106,'contacto-editado: nombre / AGENCIA CONTAKTO',1,'2019-01-31 19:46:52'),(107,'login',2,'2019-02-04 09:11:23'),(108,'candidato-creado: Juan Carlos Vargas Cordero',2,'2019-02-04 09:12:47'),(109,'candidato-editado: ARAEL FERNANDA ANGULO ATONDO',2,'2019-02-04 09:25:04'),(110,'trayectoria-nueva: Juan Carlos Vargas Cordero/AGENCIA CONTAKTO',2,'2019-02-04 09:25:31'),(111,'login',2,'2019-02-04 09:49:53'),(112,'candidato-editado: Juan Carlos Vargas Cordero',2,'2019-02-04 09:50:16'),(113,'candidato-editado: Juan Carlos Vargas Cordero',2,'2019-02-04 09:50:48'),(114,'investigacion-crear: ARAEL FERNANDA ANGULO ATONDO / GRUPO TRIMEX',2,'2019-02-04 09:51:58'),(115,'candidato-editado: Juan Carlos Vargas Cordero',2,'2019-02-04 09:53:45'),(116,'candidato-editado: Juan Carlos Vargas Cordero',2,'2019-02-04 09:54:44'),(117,'login',2,'2019-02-04 09:55:42'),(118,'candidato-editado: Juan Carlos Vargas Cordero',2,'2019-02-04 09:57:28'),(119,'candidato-editado: ARAEL FERNANDA ANGULO ATONDO',2,'2019-02-04 09:57:31'),(120,'candidato-editado: Juan Carlos Vargas Cordero',2,'2019-02-04 09:57:36'),(121,'empresas-editada: None',2,'2019-02-04 09:58:46'),(122,'logout',2,'2019-02-04 10:01:24'),(123,'login',2,'2019-02-04 10:01:44'),(124,'contacto-editado: jc / AGENCIA CONTAKTO',2,'2019-02-04 10:02:30'),(125,'contacto-editado: jc / AGENCIA CONTAKTO',2,'2019-02-04 10:02:42'),(126,'contacto-editado: jc / AGENCIA CONTAKTO',2,'2019-02-04 10:03:39'),(127,'logout',2,'2019-02-04 10:03:43'),(128,'login',2,'2019-02-04 10:03:54'),(129,'logout',2,'2019-02-04 10:03:58'),(130,'login',2,'2019-02-04 10:04:00'),(131,'logout',2,'2019-02-04 10:04:17'),(132,'login',2,'2019-02-04 10:04:29'),(133,'login',2,'2019-02-06 01:00:40'),(134,'editar-agente: Mariana',2,'2019-02-06 01:01:41'),(135,'logout',2,'2019-02-06 01:01:43'),(136,'login',2,'2019-02-06 01:02:09'),(137,'editar-agente: admint',2,'2019-02-06 01:02:46'),(138,'logout',2,'2019-02-06 01:02:51'),(139,'login',1,'2019-02-06 01:02:55'),(140,'editar-agente: Mariana',1,'2019-02-06 01:03:15'),(141,'logout',1,'2019-02-06 01:03:17'),(142,'login',4,'2019-02-06 01:03:22'),(143,'trayectoria-editar: DOMINGO ANTONIO CASILLAS BARRAGAN/MAJOR DRILLING',4,'2019-02-06 01:05:10'),(144,'trayectoria-editar: DOMINGO ANTONIO CASILLAS BARRAGAN/MAJOR DRILLING',4,'2019-02-06 01:05:21'),(145,'login',2,'2019-02-06 01:08:31'),(146,'candidato-editado: Juan Carlos Vargas Cordero',2,'2019-02-06 01:09:36'),(147,'candidato-editado: Juan Carlos Vargas Cordero',2,'2019-02-06 01:10:08'),(148,'trayectoria-editar: Juan Carlos Vargas Cordero/AGENCIA CONTAKTO',2,'2019-02-06 01:11:13'),(149,'candidato-editado: ARAEL FERNANDA ANGULO ATONDO',2,'2019-02-06 01:12:30'),(150,'candidato-editado: Juan Carlos Vargas Cordero',2,'2019-02-06 01:13:19'),(151,'login',2,'2019-02-06 01:51:15'),(152,'login',2,'2019-02-06 01:54:44'),(153,'login',2,'2019-02-06 21:36:29'),(154,'login',2,'2019-02-06 22:12:19'),(155,'login',2,'2019-02-06 22:21:21');
/*!40000 ALTER TABLE `bitacora_bitacora` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cobranza_cobranza`
--

DROP TABLE IF EXISTS `cobranza_cobranza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cobranza_cobranza` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `investigacion_id` int(11) NOT NULL,
  `monto` decimal(10,2) DEFAULT NULL,
  `folio` varchar(50) DEFAULT NULL,
  `status_cobranza` varchar(140) DEFAULT NULL,
  `last_modified` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cobranza_cobranza_e5ec9382` (`investigacion_id`),
  CONSTRAINT `investigacion_id_refs_id_6d50d9f9` FOREIGN KEY (`investigacion_id`) REFERENCES `investigacion_investigacion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cobranza_cobranza`
--

LOCK TABLES `cobranza_cobranza` WRITE;
/*!40000 ALTER TABLE `cobranza_cobranza` DISABLE KEYS */;
INSERT INTO `cobranza_cobranza` VALUES (1,1,NULL,'','0','2019-01-24 01:36:12'),(2,2,500.00,'','0','2019-01-24 01:58:26'),(3,3,NULL,'','0','2019-01-26 21:39:17'),(4,4,NULL,'','0','2019-01-29 16:28:50'),(5,5,100.00,'','0','2019-02-06 01:11:46'),(6,6,NULL,'','0','2019-02-04 09:51:58');
/*!40000 ALTER TABLE `cobranza_cobranza` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `compania_compania`
--

DROP TABLE IF EXISTS `compania_compania`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `compania_compania` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(140) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `telefono_alt` varchar(20) DEFAULT NULL,
  `email` varchar(140) DEFAULT NULL,
  `role` varchar(140) DEFAULT NULL,
  `rfc_direccion` varchar(250) DEFAULT NULL,
  `rfc` varchar(20) DEFAULT NULL,
  `notas` longtext,
  `es_cliente` tinyint(1) NOT NULL,
  `razon_social` varchar(140) DEFAULT NULL,
  `sucursal` varchar(140) DEFAULT NULL,
  `ciudad` varchar(140) DEFAULT NULL,
  `referencia_correo` int(11) DEFAULT NULL,
  `fecha_creacion` date NOT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compania_compania`
--

LOCK TABLES `compania_compania` WRITE;
/*!40000 ALTER TABLE `compania_compania` DISABLE KEYS */;
INSERT INTO `compania_compania` VALUES (1,'ABC','','','','','','','',1,'ABC','','',0,'2019-01-25',0),(2,'VSH SEGURIDAD','(662) 471-9579','','','SERVICIOS DE SEGURIDAD PRIVADA','','','',0,'SISTEMAS NOMINALES EMPRESARIALES DEL NOROESTE S.A. DE C.V.','RIO SONORA','HERMOSILLO, SONORA',2,'2019-01-25',1),(3,'GRUPO TRIMEX','','','','HARINERA','','','',1,'MOLINOS METROPOLITANOS S.A. DE C.V.','','HERMOSILLO, SONORA',0,'2019-01-25',1),(4,'ALBATROS','(662) 217-3104','6622138240','','SERVICIOS DE TRANSPORTACIÓN','','','',0,'ALBATROS AUTOBUSES S.A. DE C.V.','CENTRAL','HERMOSILLO, SONORA',2,'2019-01-30',1),(5,'HOTEL COLONIAL','(662) 259-0000','','','HOTELERO','','','',0,'OPERADORA TURISTICA DE HERMOSILLO S.A. DE C.V.','VILLA DE CERIS','HERMOSILLO, SONORA',2,'2019-01-29',1),(6,'MAJOR DRILLING','(662) 251-0265','','','SERVICIOS','','','',0,'MAJOR DRILLING DE MEXICO S.A. DE C.V.','PARQUE INDUSTRIAL','HERMOSILLO, SONORA',2,'2019-01-29',1),(7,'AGENCIA CONTAKTO','(664) 290-9306','6642909307','info@contakto.mx','SERVICIOS DE PERSONAL','','CON0909282R4','',1,'CONTAKTO-UNO S.C.','PLAYAS DE TIJUANA','TIJUANA, BAJA CALIFORNIA',2,'2019-02-04',1),(8,'CITY CLUB','(667) 753-2881','','','DEPARTAMENTAL','','','',0,'ADMINISTRACIÓN SORIANA S.A. DE C.V.','CULIACAN','CULIACAN ROSALES',2,'2019-01-29',1),(9,'test','','','','','','','',0,'','','',0,'2019-01-29',0);
/*!40000 ALTER TABLE `compania_compania` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `compania_contacto`
--

DROP TABLE IF EXISTS `compania_contacto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `compania_contacto` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `compania_id` int(11) NOT NULL,
  `nombre` varchar(140) NOT NULL,
  `puesto` varchar(140) DEFAULT NULL,
  `email` varchar(250) NOT NULL,
  `email_alt` varchar(250) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `telefono_celular` varchar(20) DEFAULT NULL,
  `telefono_otro` varchar(20) DEFAULT NULL,
  `costo_inv_laboral` double DEFAULT NULL,
  `costo_inv_completa` double DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `compania_contacto_2a71e362` (`compania_id`),
  CONSTRAINT `compania_id_refs_id_619707d6` FOREIGN KEY (`compania_id`) REFERENCES `compania_compania` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compania_contacto`
--

LOCK TABLES `compania_contacto` WRITE;
/*!40000 ALTER TABLE `compania_contacto` DISABLE KEYS */;
INSERT INTO `compania_contacto` VALUES (1,1,'Fernanda Angulo','','fernanda@contakto.mx','fernanda2@contakto.mx','6871034188','','',NULL,NULL,1),(2,3,'SARA LOURDES MENDEZ BARRIOS (-)','ENCARGADA RECLUTAMIENTO ','smendezb@gtrimex.mx','','(662) 214-9900','','',290,550,0),(3,3,'SARA LOURDES MENDEZ BARRIOS (-)','ENCARGADA RECLUTAMIENTO ','smendezb@gtrimex.mx','','(662) 214-9900','','',290,550,0),(4,3,'SARA LOURDES MENDEZ BARRIOS','ENCARGADA RECLUTAMIENTO ','smendezb@gtrimex.mx','','(662) 214-9900','','',NULL,NULL,1),(5,3,'SARA LOURDES MENDEZ BARRIOS (-)','ENCARGADA RECLUTAMIENTO ','smendezb@gtrimex.mx','','(662) 214-9900','','',NULL,NULL,0),(6,3,'SARA LOURDES MENDEZ BARRIOS (-)','ENCARGADA RECLUTAMIENTO ','smendezb@gtrimex.mx','','','','',NULL,NULL,0),(7,3,'Fernanda Angulo (-)','ENCARGADA RECLUTAMIENTO ','fernanda2@contakto.mx','','6871034188','','',NULL,NULL,0),(8,3,'ALDAIR (-)','ENCARGADA RECLUTAMIENTO ','fernanda2@contakto.mx','','6871034188','','',NULL,NULL,0),(9,7,'MARIANA MARTINEZ','GERENTE OPERATIVO','mariana@contakto.mx','','(664) 290-9306','(664) 409-1181','',0,0,1),(10,7,'ALDAIR CORTES (-)','ENCARGADO DE RECLUTAMIENTO','reclutamiento@contakto.mx','','(664) 290-9306','(664) 409-8207','',0,0,0),(11,7,'ALDAIR','ENCARGADO DE RECLUTAMIENTO','reclutamiento@contakto.mx','','(664) 290-9306','(664) 409-8207','',0,0,1),(12,7,'  (-)','','test@test.com','','','','',NULL,NULL,0),(13,7,'test (-)','test','test@test.com','','(123) 412-4213','(123) 123-1234','',NULL,NULL,0),(14,7,'nombre','puesto','prueba@gmail.com','','(123) 432-14312','(123) 412-4341','',NULL,NULL,1),(15,7,'jc','administrador','jc@hotmail.com','','(664) 290-9306','','',NULL,NULL,1);
/*!40000 ALTER TABLE `compania_contacto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_fbfc09f1` (`user_id`),
  KEY `django_admin_log_e4470c6e` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_288599e6` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c8665aa` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'site','sites','site'),(7,'migration history','south','migrationhistory'),(8,'log entry','admin','logentry'),(9,'agente info','agente','agenteinfo'),(10,'bitacora','bitacora','bitacora'),(11,'Compañia','compania','compania'),(12,'Contacto','compania','contacto'),(13,'investigacion','investigacion','investigacion'),(14,'file','persona','file'),(15,'persona','persona','persona'),(16,'telefono','persona','telefono'),(17,'direccion','persona','direccion'),(18,'prestacion vivienda','persona','prestacionvivienda'),(19,'licencia','persona','licencia'),(20,'origen','persona','origen'),(21,'info personal','persona','infopersonal'),(22,'trayectoria laboral','persona','trayectorialaboral'),(23,'legalidad','persona','legalidad'),(24,'seguro','persona','seguro'),(25,'salud','persona','salud'),(26,'actividades habitos','persona','actividadeshabitos'),(27,'academica','persona','academica'),(28,'grado escolaridad','persona','gradoescolaridad'),(29,'otro idioma','persona','otroidioma'),(30,'situacion vivienda','persona','situacionvivienda'),(31,'propietario vivienda','persona','propietariovivienda'),(32,'caractaristicas vivienda','persona','caractaristicasvivienda'),(33,'tipo inmueble','persona','tipoinmueble'),(34,'distribucion dimensiones','persona','distribuciondimensiones'),(35,'miembro marco familiar','persona','miembromarcofamiliar'),(36,'economica','persona','economica'),(37,'tarjeta credito comercial','persona','tarjetacreditocomercial'),(38,'cuenta debito','persona','cuentadebito'),(39,'automovil','persona','automovil'),(40,'bienes raices','persona','bienesraices'),(41,'deuda actual','persona','deudaactual'),(42,'referencia','persona','referencia'),(43,'cuadro evaluacion','persona','cuadroevaluacion'),(44,'documento cotejado','persona','documentocotejado'),(45,'aspecto hogar','persona','aspectohogar'),(46,'aspecto candidato','persona','aspectocandidato'),(47,'evaluacion','persona','evaluacion'),(48,'opinion','persona','opinion'),(49,'informante','persona','informante'),(50,'entrevista file','entrevista','entrevistafile'),(51,'entrevista persona','entrevista','entrevistapersona'),(52,'entrevista investigacion','entrevista','entrevistainvestigacion'),(53,'entrevista cita','entrevista','entrevistacita'),(54,'entrevista telefono','entrevista','entrevistatelefono'),(55,'entrevista direccion','entrevista','entrevistadireccion'),(56,'entrevista prestacion vivienda','entrevista','entrevistaprestacionvivienda'),(57,'entrevista licencia','entrevista','entrevistalicencia'),(58,'entrevista origen','entrevista','entrevistaorigen'),(59,'entrevista info personal','entrevista','entrevistainfopersonal'),(60,'entrevista historial en empresa','entrevista','entrevistahistorialenempresa'),(61,'entrevista salud','entrevista','entrevistasalud'),(62,'entrevista actividades habitos','entrevista','entrevistaactividadeshabitos'),(63,'entrevista academica','entrevista','entrevistaacademica'),(64,'entrevista grado escolaridad','entrevista','entrevistagradoescolaridad'),(65,'entrevista otro idioma','entrevista','entrevistaotroidioma'),(66,'entrevista situacion vivienda','entrevista','entrevistasituacionvivienda'),(67,'entrevista propietario vivienda','entrevista','entrevistapropietariovivienda'),(68,'entrevista caractaristicas vivienda','entrevista','entrevistacaractaristicasvivienda'),(69,'entrevista tipo inmueble','entrevista','entrevistatipoinmueble'),(70,'entrevista distribucion dimensiones','entrevista','entrevistadistribuciondimensiones'),(71,'entrevista miembro marco familiar','entrevista','entrevistamiembromarcofamiliar'),(72,'entrevista economica','entrevista','entrevistaeconomica'),(73,'entrevista tarjeta credito comercial','entrevista','entrevistatarjetacreditocomercial'),(74,'entrevista cuenta debito','entrevista','entrevistacuentadebito'),(75,'entrevista automovil','entrevista','entrevistaautomovil'),(76,'entrevista bienes raices','entrevista','entrevistabienesraices'),(77,'entrevista seguro','entrevista','entrevistaseguro'),(78,'entrevista deuda actual','entrevista','entrevistadeudaactual'),(79,'entrevista referencia','entrevista','entrevistareferencia'),(80,'entrevista documento cotejado','entrevista','entrevistadocumentocotejado'),(81,'entrevista aspecto hogar','entrevista','entrevistaaspectohogar'),(82,'entrevista aspecto candidato','entrevista','entrevistaaspectocandidato'),(83,'cobranza','cobranza','cobranza'),(84,'adjuntos','adjuntos','adjuntos');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_c25c2c28` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('1ef405988839923b8a393c2ee95e25c1','YTdhNjA2ODA5MDVjNjAzMTZiMjI4OWMzMWQ4Njc0MGU1OThjYjI5NTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZFUuYXBwLmZyb250LmJhY2tlbmRzLkVtYWlsT3JVc2VybmFtZU1vZGVsQmFja2Vu\nZFUNX2F1dGhfdXNlcl9pZIoBAVUOZmlsdHJvc19zZWFyY2h9cQIoVQlzdGF0dXNfaWRYAQAAADNV\nC2ZlY2hhX2ZpbmFsWAAAAABVDGZlY2hhX2luaWNpb1gAAAAAVQtjb21wYW5pYV9pZFgAAAAAVQ9j\nb21wYW5pYV9ub21icmVYAAAAAFUGbm9tYnJlWAAAAABVCWFnZW50ZV9pZFgAAAAAdVUVZmlsdHJv\nc19zZWFyY2hfYWdlbnRlfXEDKFUJc3RhdHVzX2lkcQRYAQAAADBVC2ZlY2hhX2ZpbmFscQVYAAAA\nAFUMZmVjaGFfaW5pY2lvcQZYAAAAAFULY29tcGFuaWFfaWRxB1gAAAAAVQ9jb21wYW5pYV9ub21i\ncmVxCFgAAAAAVQlhZ2VudGVfaWRxCVgAAAAAdXUu\n','2019-02-23 21:06:08'),('530cce22230a0dd7dda1b0b4ace1bb00','ZWM4N2IwNTFlZTYwNWVjOWYzMGVkMmFhZDA2ZTg1MTdmZjY5MTFjMjqAAn1xAS4=\n','2019-02-01 23:23:57'),('5efd85bae887838f19e71a42a15873e1','OTQ5MTk2YWNmMmM0OWY3NjdmYzlhNzQwOWI3YTgwZjcyOTQ0ZjQ2YjqAAn1xAShVDmZpbHRyb3Nf\nc2VhcmNofXECKFUJc3RhdHVzX2lkcQNYAAAAAFULZmVjaGFfZmluYWxxBFgAAAAAVQxmZWNoYV9p\nbmljaW9xBVgAAAAAVQtjb21wYW5pYV9pZHEGWAAAAABVD2NvbXBhbmlhX25vbWJyZXEHWAAAAABV\nBm5vbWJyZXEIWAAAAABVCWFnZW50ZV9pZHEJWAAAAAB1VQ1fYXV0aF91c2VyX2lkigECVRJfYXV0\naF91c2VyX2JhY2tlbmRVLmFwcC5mcm9udC5iYWNrZW5kcy5FbWFpbE9yVXNlcm5hbWVNb2RlbEJh\nY2tlbmRVFWZpbHRyb3Nfc2VhcmNoX2FnZW50ZX1xCihVCXN0YXR1c19pZFgBAAAAMFULZmVjaGFf\nZmluYWxYAAAAAFUMZmVjaGFfaW5pY2lvWAAAAABVC2NvbXBhbmlhX2lkWAAAAABVD2NvbXBhbmlh\nX25vbWJyZVgAAAAAVQlhZ2VudGVfaWRYAQAAADJ1dS4=\n','2019-02-20 22:21:37'),('b0f58d2d712a3f27c432fa1b481ed03c','OWQ1YzIyYjBjODEwYWJiMjk0NTQwNGFmNjk2YWE4ZDc5YzMxM2I3MzqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZFUuYXBwLmZyb250LmJhY2tlbmRzLkVtYWlsT3JVc2VybmFtZU1vZGVsQmFja2Vu\nZFUNX2F1dGhfdXNlcl9pZIoBAlUOZmlsdHJvc19zZWFyY2h9cQIoVQlzdGF0dXNfaWRxA1gBAAAA\nM1ULZmVjaGFfZmluYWxxBFgAAAAAVQxmZWNoYV9pbmljaW9xBVgAAAAAVQtjb21wYW5pYV9pZHEG\nWAAAAABVD2NvbXBhbmlhX25vbWJyZXEHWAAAAABVBm5vbWJyZXEIWAAAAABVCWFnZW50ZV9pZHEJ\nWAAAAAB1dS4=\n','2019-02-20 22:12:30');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistaacademica`
--

DROP TABLE IF EXISTS `entrevista_entrevistaacademica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistaacademica` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `cedula_profesional` varchar(200) DEFAULT NULL,
  `cedula_prof_ano_exp` varchar(200) DEFAULT NULL,
  `estudios_actuales` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistaacademica_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_7c20973f` FOREIGN KEY (`person_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistaacademica`
--

LOCK TABLES `entrevista_entrevistaacademica` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistaacademica` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistaacademica` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistaactividadeshabitos`
--

DROP TABLE IF EXISTS `entrevista_entrevistaactividadeshabitos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistaactividadeshabitos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persona_id` int(11) NOT NULL,
  `tiempo_libre` varchar(140) DEFAULT NULL,
  `extras` varchar(140) DEFAULT NULL,
  `frecuencia_tabaco` varchar(140) DEFAULT NULL,
  `frecuencia_alcohol` varchar(140) DEFAULT NULL,
  `frecuencia_otras_sust` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistaactividadeshabitos_e27cbd6d` (`persona_id`),
  CONSTRAINT `persona_id_refs_id_3abc3653` FOREIGN KEY (`persona_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistaactividadeshabitos`
--

LOCK TABLES `entrevista_entrevistaactividadeshabitos` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistaactividadeshabitos` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistaactividadeshabitos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistaaspectocandidato`
--

DROP TABLE IF EXISTS `entrevista_entrevistaaspectocandidato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistaaspectocandidato` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `estatus` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistaaspectocandidato_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_78fc3c4a` FOREIGN KEY (`person_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistaaspectocandidato`
--

LOCK TABLES `entrevista_entrevistaaspectocandidato` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistaaspectocandidato` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistaaspectocandidato` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistaaspectohogar`
--

DROP TABLE IF EXISTS `entrevista_entrevistaaspectohogar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistaaspectohogar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `estatus` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistaaspectohogar_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_e8d94d70` FOREIGN KEY (`person_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistaaspectohogar`
--

LOCK TABLES `entrevista_entrevistaaspectohogar` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistaaspectohogar` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistaaspectohogar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistaautomovil`
--

DROP TABLE IF EXISTS `entrevista_entrevistaautomovil`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistaautomovil` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `marca` varchar(140) DEFAULT NULL,
  `modelo_ano` varchar(140) DEFAULT NULL,
  `liquidacion` varchar(140) DEFAULT NULL,
  `valor_comercial` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistaautomovil_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_43f4a875` FOREIGN KEY (`person_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistaautomovil`
--

LOCK TABLES `entrevista_entrevistaautomovil` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistaautomovil` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistaautomovil` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistabienesraices`
--

DROP TABLE IF EXISTS `entrevista_entrevistabienesraices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistabienesraices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `tipo_inmueble` varchar(140) DEFAULT NULL,
  `ubicacion` varchar(140) DEFAULT NULL,
  `liquidacion` varchar(140) DEFAULT NULL,
  `valor_comercial` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistabienesraices_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_4fb971f9` FOREIGN KEY (`person_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistabienesraices`
--

LOCK TABLES `entrevista_entrevistabienesraices` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistabienesraices` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistabienesraices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistacaractaristicasvivienda`
--

DROP TABLE IF EXISTS `entrevista_entrevistacaractaristicasvivienda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistacaractaristicasvivienda` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `propia` varchar(50) DEFAULT NULL,
  `rentada` varchar(50) DEFAULT NULL,
  `hipotecada` varchar(50) DEFAULT NULL,
  `prestada` varchar(50) DEFAULT NULL,
  `otra` varchar(50) DEFAULT NULL,
  `valor_aproximado` varchar(50) DEFAULT NULL,
  `renta_mensual` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistacaractaristicasvivienda_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_6e83b780` FOREIGN KEY (`person_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistacaractaristicasvivienda`
--

LOCK TABLES `entrevista_entrevistacaractaristicasvivienda` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistacaractaristicasvivienda` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistacaractaristicasvivienda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistacita`
--

DROP TABLE IF EXISTS `entrevista_entrevistacita`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistacita` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `investigacion_id` int(11) NOT NULL,
  `fecha_entrevista` date DEFAULT NULL,
  `hora_entrevista` time DEFAULT NULL,
  `entrevistador` varchar(200) DEFAULT NULL,
  `autorizada` int(11) DEFAULT NULL,
  `observaciones` longtext,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistacita_e5ec9382` (`investigacion_id`),
  CONSTRAINT `investigacion_id_refs_id_9d008dc4` FOREIGN KEY (`investigacion_id`) REFERENCES `investigacion_investigacion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistacita`
--

LOCK TABLES `entrevista_entrevistacita` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistacita` DISABLE KEYS */;
INSERT INTO `entrevista_entrevistacita` VALUES (1,1,NULL,NULL,'',NULL,''),(2,2,'2012-12-02','00:30:00','',1,''),(3,3,NULL,NULL,'',2,''),(4,4,NULL,NULL,'',1,''),(5,5,'2012-12-12','01:30:00','rafael garcia',1,'45454'),(6,6,NULL,NULL,NULL,0,NULL);
/*!40000 ALTER TABLE `entrevista_entrevistacita` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistacuentadebito`
--

DROP TABLE IF EXISTS `entrevista_entrevistacuentadebito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistacuentadebito` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `institucion` varchar(140) DEFAULT NULL,
  `saldo_mensual` varchar(140) DEFAULT NULL,
  `antiguedad` varchar(140) DEFAULT NULL,
  `ahorro` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistacuentadebito_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_6ebf136d` FOREIGN KEY (`person_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistacuentadebito`
--

LOCK TABLES `entrevista_entrevistacuentadebito` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistacuentadebito` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistacuentadebito` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistadeudaactual`
--

DROP TABLE IF EXISTS `entrevista_entrevistadeudaactual`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistadeudaactual` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `fecha_otorgamiento` varchar(140) DEFAULT NULL,
  `tipo` varchar(140) DEFAULT NULL,
  `institucion` varchar(140) DEFAULT NULL,
  `cantidad_total` varchar(140) DEFAULT NULL,
  `saldo_actual` varchar(140) DEFAULT NULL,
  `pago_mensual` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistadeudaactual_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_e174989c` FOREIGN KEY (`person_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistadeudaactual`
--

LOCK TABLES `entrevista_entrevistadeudaactual` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistadeudaactual` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistadeudaactual` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistadireccion`
--

DROP TABLE IF EXISTS `entrevista_entrevistadireccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistadireccion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persona_id` int(11) NOT NULL,
  `calle` varchar(140) DEFAULT NULL,
  `ciudad` varchar(140) DEFAULT NULL,
  `colonia` varchar(140) DEFAULT NULL,
  `cp` varchar(140) DEFAULT NULL,
  `estado` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistadireccion_e27cbd6d` (`persona_id`),
  CONSTRAINT `persona_id_refs_id_b4b558eb` FOREIGN KEY (`persona_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistadireccion`
--

LOCK TABLES `entrevista_entrevistadireccion` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistadireccion` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistadireccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistadistribuciondimensiones`
--

DROP TABLE IF EXISTS `entrevista_entrevistadistribuciondimensiones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistadistribuciondimensiones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `habitaciones` varchar(50) DEFAULT NULL,
  `banos` varchar(50) DEFAULT NULL,
  `salas` varchar(50) DEFAULT NULL,
  `comedor` varchar(50) DEFAULT NULL,
  `cocina` varchar(50) DEFAULT NULL,
  `patios` varchar(50) DEFAULT NULL,
  `cocheras` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistadistribuciondimensiones_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_6dd07ba0` FOREIGN KEY (`person_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistadistribuciondimensiones`
--

LOCK TABLES `entrevista_entrevistadistribuciondimensiones` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistadistribuciondimensiones` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistadistribuciondimensiones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistadocumentocotejado`
--

DROP TABLE IF EXISTS `entrevista_entrevistadocumentocotejado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistadocumentocotejado` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `estatus` tinyint(1) NOT NULL,
  `observaciones` longtext,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistadocumentocotejado_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_76f03766` FOREIGN KEY (`person_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistadocumentocotejado`
--

LOCK TABLES `entrevista_entrevistadocumentocotejado` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistadocumentocotejado` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistadocumentocotejado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistaeconomica`
--

DROP TABLE IF EXISTS `entrevista_entrevistaeconomica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistaeconomica` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `concepto` varchar(140) NOT NULL,
  `monto` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistaeconomica_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_2f6d7923` FOREIGN KEY (`person_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=862 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistaeconomica`
--

LOCK TABLES `entrevista_entrevistaeconomica` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistaeconomica` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistaeconomica` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistafile`
--

DROP TABLE IF EXISTS `entrevista_entrevistafile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistafile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `record` varchar(100) NOT NULL,
  `fecha_registro` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistafile`
--

LOCK TABLES `entrevista_entrevistafile` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistafile` DISABLE KEYS */;
INSERT INTO `entrevista_entrevistafile` VALUES (1,'xls/FORMATO_ESC_CON_PUNTOS_1_1.xlsx','2019-01-24'),(2,'xls/FORMATO_ESC_CON_PUNTOS_1_2.xlsx','2019-01-24'),(3,'xls/FORMATO_ESC_CON_PUNTOS_1_3.xlsx','2019-01-24'),(4,'xls/rrrr.xlsx','2019-01-24'),(5,'xls/ESC_ARAEL_FERNANDA_ANGULO.xlsx','2019-01-29'),(6,'xls/ESC_ARAEL_FERNANDA_ANGULO_1.xlsx','2019-01-29'),(7,'xls/ESC_ARAEL_FERNANDA_ANGULO_2.xlsx','2019-01-29'),(8,'xls/ESC_ARAEL_FERNANDA_ANGULO_3.xlsx','2019-01-29'),(9,'xls/ESC_ARAEL_FERNANDA_ANGULO_4.xlsx','2019-01-29'),(10,'xls/FORMATO_ESC_LLENO_4.xlsx','2019-02-04'),(11,'xls/FORMATO_ESC_EN_BLANCO_14.xlsx','2019-02-04'),(12,'xls/PV2.2_11.xlsx','2019-02-04'),(13,'xls/PV2_25.xlsx','2019-02-04'),(14,'xls/FORMATO_ESC_CON_PUNTOS_9.xlsx','2019-02-04'),(15,'xls/PV2.2_12.xlsx','2019-02-04'),(16,'xls/FORMATO_ESC_CON_PUNTOS_10.xlsx','2019-02-04'),(17,'xls/FORMATO_ESC_EN_BLANCO_15.xlsx','2019-02-04'),(18,'xls/FORMATO_ESC_LLENO_5.xlsx','2019-02-04'),(19,'xls/FORMATO_ESC_MINUSCULAS_2.xlsx','2019-02-04'),(20,'xls/FORMATO_ESC.xlsx','2019-02-04'),(21,'xls/PV2_26.xlsx','2019-02-04'),(22,'xls/ESC_Jose_Luis_Sandoval_Lamadrid.xlsx','2019-02-04'),(23,'xls/PV.xlsx','2019-02-04'),(24,'xls/PV2_27.xlsx','2019-02-04'),(25,'xls/PV2_NUMERICO_17.xlsx','2019-02-04'),(26,'xls/FORMATO_ESC_1.xlsx','2019-02-04'),(27,'xls/SISTEMA2.xlsx','2019-02-04'),(28,'xls/ESC_Jose_Luis_Sandoval_Lamadrid_1.xlsx','2019-02-04'),(29,'xls/PV_1.xlsx','2019-02-04'),(30,'xls/PV_2.xlsx','2019-02-04'),(31,'xls/report.xlsx','2019-02-04'),(32,'xls/FORMATO_ESC_2.xlsx','2019-02-04'),(33,'xls/FORMATO_ESC_CON_PUNTOS_1_4.xlsx','2019-02-04'),(34,'xls/FORMATO_ESC_CON_PUNTOS_1_5.xlsx','2019-02-04'),(35,'xls/FORMATO_SISTEMA.xlsx','2019-02-04'),(36,'xls/FORMATO_ESC_LLENO_6.xlsx','2019-02-04'),(37,'xls/FORMATO_ESC_CON_PUNTOS_1_6.xlsx','2019-02-04'),(38,'xls/FORMATO_ESC_CON_PUNTOS_1_7.xlsx','2019-02-04'),(39,'xls/FORMATO_ESC_CON_PUNTOS_2.xls','2019-02-04'),(40,'xls/FORMATO_ESC_CON_PUNTOS_1_8.xlsx','2019-02-05'),(41,'xls/FORMATO_ESC_CON_PUNTOS_1_9.xlsx','2019-02-05'),(42,'xls/FORMATO_ESC_LLENO_7.xlsx','2019-02-05'),(43,'xls/FORMATO_ESC_LLENO_8.xlsx','2019-02-05'),(44,'xls/ESC_ARAEL_FERNANDA_ANGULO_5.xlsx','2019-02-05'),(45,'xls/ESC_ARAEL_FERNANDA_ANGULO_6.xlsx','2019-02-05');
/*!40000 ALTER TABLE `entrevista_entrevistafile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistagradoescolaridad`
--

DROP TABLE IF EXISTS `entrevista_entrevistagradoescolaridad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistagradoescolaridad` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `grado` varchar(20) NOT NULL,
  `institucion` varchar(200) DEFAULT NULL,
  `ciudad` varchar(200) DEFAULT NULL,
  `anos` varchar(200) DEFAULT NULL,
  `certificado` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistagradoescolaridad_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_55c9160c` FOREIGN KEY (`person_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=206 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistagradoescolaridad`
--

LOCK TABLES `entrevista_entrevistagradoescolaridad` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistagradoescolaridad` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistagradoescolaridad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistahistorialenempresa`
--

DROP TABLE IF EXISTS `entrevista_entrevistahistorialenempresa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistahistorialenempresa` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persona_id` int(11) NOT NULL,
  `categoria` varchar(20) NOT NULL,
  `tiene` varchar(140) DEFAULT NULL,
  `puesto` varchar(500) DEFAULT NULL,
  `periodo` varchar(500) DEFAULT NULL,
  `nombre` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistahistorialenempresa_e27cbd6d` (`persona_id`),
  CONSTRAINT `persona_id_refs_id_7510a1e5` FOREIGN KEY (`persona_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistahistorialenempresa`
--

LOCK TABLES `entrevista_entrevistahistorialenempresa` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistahistorialenempresa` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistahistorialenempresa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistainfopersonal`
--

DROP TABLE IF EXISTS `entrevista_entrevistainfopersonal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistainfopersonal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persona_id` int(11) NOT NULL,
  `objetivo_personal` varchar(500) NOT NULL,
  `objetivo_en_empresa` varchar(500) DEFAULT NULL,
  `cualidades` varchar(500) DEFAULT NULL,
  `defectos` varchar(500) DEFAULT NULL,
  `trabajo_que_desarrolla` varchar(500) DEFAULT NULL,
  `antecedentes_penales` varchar(500) DEFAULT NULL,
  `tatuajes` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistainfopersonal_e27cbd6d` (`persona_id`),
  CONSTRAINT `persona_id_refs_id_c12febee` FOREIGN KEY (`persona_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistainfopersonal`
--

LOCK TABLES `entrevista_entrevistainfopersonal` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistainfopersonal` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistainfopersonal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistainvestigacion`
--

DROP TABLE IF EXISTS `entrevista_entrevistainvestigacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistainvestigacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `agente_id` int(11) NOT NULL,
  `persona_id` int(11) NOT NULL,
  `empresa_contratante` varchar(140) DEFAULT NULL,
  `fecha_recibido` varchar(140) DEFAULT NULL,
  `puesto` varchar(140) DEFAULT NULL,
  `fecha_registro` varchar(140) DEFAULT NULL,
  `conclusiones` longtext NOT NULL,
  `resultado` varchar(30) DEFAULT NULL,
  `archivo_id` int(11) DEFAULT NULL,
  `folio` varchar(50) DEFAULT NULL,
  `presupuesto` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistainvestigacion_730b2c6a` (`agente_id`),
  KEY `entrevista_entrevistainvestigacion_e27cbd6d` (`persona_id`),
  KEY `entrevista_entrevistainvestigacion_3add06a9` (`archivo_id`),
  CONSTRAINT `agente_id_refs_id_b437d66e` FOREIGN KEY (`agente_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `archivo_id_refs_id_ae4d1f8d` FOREIGN KEY (`archivo_id`) REFERENCES `entrevista_entrevistafile` (`id`),
  CONSTRAINT `persona_id_refs_id_b5f3a0ac` FOREIGN KEY (`persona_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistainvestigacion`
--

LOCK TABLES `entrevista_entrevistainvestigacion` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistainvestigacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistainvestigacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistalicencia`
--

DROP TABLE IF EXISTS `entrevista_entrevistalicencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistalicencia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persona_id` int(11) NOT NULL,
  `numero` varchar(20) DEFAULT NULL,
  `tipo` varchar(14) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistalicencia_e27cbd6d` (`persona_id`),
  CONSTRAINT `persona_id_refs_id_b500e6ac` FOREIGN KEY (`persona_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistalicencia`
--

LOCK TABLES `entrevista_entrevistalicencia` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistalicencia` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistalicencia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistamiembromarcofamiliar`
--

DROP TABLE IF EXISTS `entrevista_entrevistamiembromarcofamiliar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistamiembromarcofamiliar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `nombre` varchar(140) DEFAULT NULL,
  `edad` varchar(140) DEFAULT NULL,
  `ocupacion` varchar(140) DEFAULT NULL,
  `empresa` varchar(140) DEFAULT NULL,
  `residencia` varchar(140) DEFAULT NULL,
  `telefono` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistamiembromarcofamiliar_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_1a84b01c` FOREIGN KEY (`person_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=575 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistamiembromarcofamiliar`
--

LOCK TABLES `entrevista_entrevistamiembromarcofamiliar` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistamiembromarcofamiliar` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistamiembromarcofamiliar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistaorigen`
--

DROP TABLE IF EXISTS `entrevista_entrevistaorigen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistaorigen` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persona_id` int(11) NOT NULL,
  `lugar` varchar(140) DEFAULT NULL,
  `nacionalidad` varchar(140) DEFAULT NULL,
  `fecha` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistaorigen_e27cbd6d` (`persona_id`),
  CONSTRAINT `persona_id_refs_id_cde33886` FOREIGN KEY (`persona_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistaorigen`
--

LOCK TABLES `entrevista_entrevistaorigen` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistaorigen` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistaorigen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistaotroidioma`
--

DROP TABLE IF EXISTS `entrevista_entrevistaotroidioma`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistaotroidioma` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `porcentaje` varchar(140) DEFAULT NULL,
  `idioma` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistaotroidioma_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_79128167` FOREIGN KEY (`person_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistaotroidioma`
--

LOCK TABLES `entrevista_entrevistaotroidioma` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistaotroidioma` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistaotroidioma` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistapersona`
--

DROP TABLE IF EXISTS `entrevista_entrevistapersona`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistapersona` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `investigacion_id` int(11) NOT NULL,
  `nombre` varchar(140) NOT NULL,
  `nss` varchar(30) DEFAULT NULL,
  `edad` varchar(140) DEFAULT NULL,
  `curp` varchar(30) DEFAULT NULL,
  `rfc` varchar(30) DEFAULT NULL,
  `ife` varchar(30) DEFAULT NULL,
  `pasaporte` varchar(30) DEFAULT NULL,
  `smn` varchar(30) DEFAULT NULL,
  `estado_civil` varchar(100) DEFAULT NULL,
  `fecha_matrimonio` varchar(100) DEFAULT NULL,
  `religion` varchar(140) NOT NULL,
  `tiempo_radicando` varchar(140) DEFAULT NULL,
  `medio_utilizado` varchar(140) DEFAULT NULL,
  `fecha_registro` date NOT NULL,
  `activa` tinyint(1) NOT NULL,
  `dependientes_economicos` longtext,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistapersona_e5ec9382` (`investigacion_id`),
  CONSTRAINT `investigacion_id_refs_id_7331466` FOREIGN KEY (`investigacion_id`) REFERENCES `investigacion_investigacion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistapersona`
--

LOCK TABLES `entrevista_entrevistapersona` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistapersona` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistapersona` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistaprestacionvivienda`
--

DROP TABLE IF EXISTS `entrevista_entrevistaprestacionvivienda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistaprestacionvivienda` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persona_id` int(11) NOT NULL,
  `categoria_viv` varchar(20) NOT NULL,
  `activo` varchar(140) DEFAULT NULL,
  `fecha_tramite` varchar(140) DEFAULT NULL,
  `numero_credito` varchar(140) DEFAULT NULL,
  `uso` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistaprestacionvivienda_e27cbd6d` (`persona_id`),
  CONSTRAINT `persona_id_refs_id_59ead2dc` FOREIGN KEY (`persona_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistaprestacionvivienda`
--

LOCK TABLES `entrevista_entrevistaprestacionvivienda` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistaprestacionvivienda` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistaprestacionvivienda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistapropietariovivienda`
--

DROP TABLE IF EXISTS `entrevista_entrevistapropietariovivienda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistapropietariovivienda` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `nombre` varchar(200) DEFAULT NULL,
  `parentesco` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistapropietariovivienda_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_ad3a9a55` FOREIGN KEY (`person_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistapropietariovivienda`
--

LOCK TABLES `entrevista_entrevistapropietariovivienda` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistapropietariovivienda` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistapropietariovivienda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistareferencia`
--

DROP TABLE IF EXISTS `entrevista_entrevistareferencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistareferencia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `nombre` varchar(140) DEFAULT NULL,
  `domicilio` varchar(200) DEFAULT NULL,
  `telefono` varchar(140) DEFAULT NULL,
  `tiempo_conocido` varchar(140) DEFAULT NULL,
  `parentesco` varchar(140) DEFAULT NULL,
  `ocupacion` varchar(140) DEFAULT NULL,
  `lugares_labor_evaluado` varchar(200) DEFAULT NULL,
  `opinion` longtext,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistareferencia_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_918b72d4` FOREIGN KEY (`person_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistareferencia`
--

LOCK TABLES `entrevista_entrevistareferencia` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistareferencia` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistareferencia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistasalud`
--

DROP TABLE IF EXISTS `entrevista_entrevistasalud`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistasalud` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persona_id` int(11) NOT NULL,
  `peso_kg` varchar(200) DEFAULT NULL,
  `estatura_mts` varchar(200) DEFAULT NULL,
  `salud_fisica` varchar(200) DEFAULT NULL,
  `salud_visual` varchar(200) DEFAULT NULL,
  `embarazo_meses` varchar(200) DEFAULT NULL,
  `ejercicio_tipo_frecuencia` varchar(200) DEFAULT NULL,
  `accidentes` varchar(200) DEFAULT NULL,
  `intervenciones_quirurgicas` varchar(200) DEFAULT NULL,
  `enfermedades_familiares` varchar(200) DEFAULT NULL,
  `tratamiento_medico_psicologico` varchar(200) DEFAULT NULL,
  `enfermedades_mayor_frecuencia` varchar(200) DEFAULT NULL,
  `institucion_medica` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistasalud_e27cbd6d` (`persona_id`),
  CONSTRAINT `persona_id_refs_id_d07fa470` FOREIGN KEY (`persona_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistasalud`
--

LOCK TABLES `entrevista_entrevistasalud` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistasalud` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistasalud` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistaseguro`
--

DROP TABLE IF EXISTS `entrevista_entrevistaseguro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistaseguro` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `empresa` varchar(140) DEFAULT NULL,
  `tipo` varchar(140) DEFAULT NULL,
  `forma_pago` varchar(140) DEFAULT NULL,
  `vigencia` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistaseguro_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_de229c13` FOREIGN KEY (`person_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistaseguro`
--

LOCK TABLES `entrevista_entrevistaseguro` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistaseguro` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistaseguro` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistasituacionvivienda`
--

DROP TABLE IF EXISTS `entrevista_entrevistasituacionvivienda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistasituacionvivienda` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `tiempo_radicando` varchar(50) DEFAULT NULL,
  `tipo_mobiliario` varchar(200) DEFAULT NULL,
  `sector_socioeconomico` varchar(200) DEFAULT NULL,
  `personas_viven_con_evaluado` varchar(50) DEFAULT NULL,
  `conservacion` varchar(200) DEFAULT NULL,
  `tamano_aprox_mts2` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistasituacionvivienda_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_729d6472` FOREIGN KEY (`person_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistasituacionvivienda`
--

LOCK TABLES `entrevista_entrevistasituacionvivienda` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistasituacionvivienda` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistasituacionvivienda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistatarjetacreditocomercial`
--

DROP TABLE IF EXISTS `entrevista_entrevistatarjetacreditocomercial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistatarjetacreditocomercial` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `institucion` varchar(140) DEFAULT NULL,
  `limite_credito` varchar(140) DEFAULT NULL,
  `pago_minimo` varchar(140) DEFAULT NULL,
  `saldo_actual` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistatarjetacreditocomercial_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_d5657337` FOREIGN KEY (`person_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=83 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistatarjetacreditocomercial`
--

LOCK TABLES `entrevista_entrevistatarjetacreditocomercial` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistatarjetacreditocomercial` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistatarjetacreditocomercial` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistatelefono`
--

DROP TABLE IF EXISTS `entrevista_entrevistatelefono`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistatelefono` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persona_id` int(11) NOT NULL,
  `categoria` varchar(20) NOT NULL,
  `numero` varchar(20) DEFAULT NULL,
  `parentesco` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistatelefono_e27cbd6d` (`persona_id`),
  CONSTRAINT `persona_id_refs_id_a2f7d9e2` FOREIGN KEY (`persona_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=159 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistatelefono`
--

LOCK TABLES `entrevista_entrevistatelefono` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistatelefono` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistatelefono` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrevista_entrevistatipoinmueble`
--

DROP TABLE IF EXISTS `entrevista_entrevistatipoinmueble`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entrevista_entrevistatipoinmueble` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `casa` varchar(50) DEFAULT NULL,
  `terreno_compartido` varchar(50) DEFAULT NULL,
  `departamento` varchar(50) DEFAULT NULL,
  `vivienda_popular` varchar(50) DEFAULT NULL,
  `otro_tipo` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `entrevista_entrevistatipoinmueble_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_854dae4f` FOREIGN KEY (`person_id`) REFERENCES `entrevista_entrevistapersona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrevista_entrevistatipoinmueble`
--

LOCK TABLES `entrevista_entrevistatipoinmueble` WRITE;
/*!40000 ALTER TABLE `entrevista_entrevistatipoinmueble` DISABLE KEYS */;
/*!40000 ALTER TABLE `entrevista_entrevistatipoinmueble` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `investigacion_investigacion`
--

DROP TABLE IF EXISTS `investigacion_investigacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `investigacion_investigacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `agente_id` int(11) NOT NULL,
  `candidato_id` int(11) NOT NULL,
  `compania_id` int(11) NOT NULL,
  `contacto_id` int(11) NOT NULL,
  `fecha_recibido` date DEFAULT NULL,
  `puesto` varchar(140) NOT NULL,
  `observaciones` longtext,
  `entrevista` datetime DEFAULT NULL,
  `fecha_registro` date NOT NULL,
  `last_modified` datetime DEFAULT NULL,
  `conclusiones` longtext,
  `resultado` varchar(30) DEFAULT NULL,
  `archivo_id` int(11) DEFAULT NULL,
  `folio` varchar(50) DEFAULT NULL,
  `presupuesto` varchar(50) DEFAULT NULL,
  `status` varchar(140) DEFAULT NULL,
  `status_active` tinyint(1) NOT NULL,
  `status_general` varchar(140) DEFAULT NULL,
  `observaciones_generales` longtext,
  `tipo_investigacion_status` int(11) DEFAULT NULL,
  `tipo_investigacion_texto` longtext,
  `laboro_anteriormente` int(11) DEFAULT NULL,
  `familiar_laborando` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `investigacion_investigacion_730b2c6a` (`agente_id`),
  KEY `investigacion_investigacion_6e7c0fd4` (`candidato_id`),
  KEY `investigacion_investigacion_2a71e362` (`compania_id`),
  KEY `investigacion_investigacion_37f80fed` (`contacto_id`),
  KEY `investigacion_investigacion_3add06a9` (`archivo_id`),
  CONSTRAINT `agente_id_refs_id_f07599d6` FOREIGN KEY (`agente_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `archivo_id_refs_id_bd371156` FOREIGN KEY (`archivo_id`) REFERENCES `persona_file` (`id`),
  CONSTRAINT `candidato_id_refs_id_db4fe2c9` FOREIGN KEY (`candidato_id`) REFERENCES `persona_persona` (`id`),
  CONSTRAINT `compania_id_refs_id_3623e185` FOREIGN KEY (`compania_id`) REFERENCES `compania_compania` (`id`),
  CONSTRAINT `contacto_id_refs_id_7680c768` FOREIGN KEY (`contacto_id`) REFERENCES `compania_contacto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `investigacion_investigacion`
--

LOCK TABLES `investigacion_investigacion` WRITE;
/*!40000 ALTER TABLE `investigacion_investigacion` DISABLE KEYS */;
INSERT INTO `investigacion_investigacion` VALUES (1,2,1,1,1,'2019-01-22','ADMIN','',NULL,'2019-01-23','2019-01-24 01:46:30','','1',NULL,NULL,NULL,'2',0,'2',NULL,NULL,'',0,0),(2,2,2,1,1,'2019-01-29','ADMIN','',NULL,'2019-01-23','2019-01-25 16:53:58','','0',NULL,NULL,NULL,'1',0,'2','ashdjkashdljksa\r\n\r\nentrevosas 120/01/18 3pm',1,'',0,0),(3,4,3,3,4,'2018-10-03','CARGADOR MANIOBRISTA','',NULL,'2019-01-26','2019-01-29 15:56:52','EL CANDIDATO CUENTA CON PERIODOS DE INACTIVIDAD MUY LARGOS QUE DIFICULTAN PROFUNDIZAR SU INVESTIGACIÓN LABORAL Y NO PROPORCIONA INFORMACIÓN O CONTACTOS QUE VALIDEN SUS NEGOCIOS PROPIOS. ADEMÁS, FUE IMPOSIBLE OBTENER SUS SEMANAS COTIZADAS PARA VALIDAR ESOS PERIODOS NO REPORTADOS.','3',NULL,NULL,NULL,'2',1,'1',NULL,1,'EL CANDIDATO REPORTA HABER LABORADO POR SU CUENTA DURANTE SUS PERIODOS DE INACTIVIDAD LABORAL, SIN EMBARGO, NO TIENE CONTACTOS QUE VALIDEN ESTA INFORMACIÓN.\r\nNO SE LOGRARON OBTENER LAS SEMANAS COTIZADAS DEL CANDIDATO.',2,2),(4,1,4,7,15,'2018-07-19','AUXILIAR DE RECURSOS HUMANOS','',NULL,'2019-01-29','2019-02-06 01:14:26','','0',NULL,NULL,NULL,'0',1,'0',NULL,2,'',2,2),(5,1,5,3,4,'2019-02-04','Gerente de Ventas','',NULL,'2019-02-04','2019-02-06 01:13:19','454545','0',NULL,NULL,NULL,'0',1,'0','todo mal',1,'',1,1),(6,1,4,3,4,'2019-02-04','Rh','',NULL,'2019-02-04','2019-02-04 09:51:58',NULL,'0',NULL,NULL,NULL,'0',1,'0',NULL,NULL,'',NULL,NULL);
/*!40000 ALTER TABLE `investigacion_investigacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_academica`
--

DROP TABLE IF EXISTS `persona_academica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_academica` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `cedula_profesional` varchar(200) NOT NULL,
  `cedula_prof_ano_exp` varchar(200) NOT NULL,
  `estudios_actuales` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_academica_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_6e227b1d` FOREIGN KEY (`person_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_academica`
--

LOCK TABLES `persona_academica` WRITE;
/*!40000 ALTER TABLE `persona_academica` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_academica` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_actividadeshabitos`
--

DROP TABLE IF EXISTS `persona_actividadeshabitos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_actividadeshabitos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persona_id` int(11) NOT NULL,
  `tiempo_libre` varchar(140) NOT NULL,
  `extras` varchar(140) NOT NULL,
  `frecuencia_tabaco` varchar(140) NOT NULL,
  `frecuencia_alcohol` varchar(140) NOT NULL,
  `frecuencia_otras_sust` varchar(140) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_actividadeshabitos_e27cbd6d` (`persona_id`),
  CONSTRAINT `persona_id_refs_id_12644c0f` FOREIGN KEY (`persona_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_actividadeshabitos`
--

LOCK TABLES `persona_actividadeshabitos` WRITE;
/*!40000 ALTER TABLE `persona_actividadeshabitos` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_actividadeshabitos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_aspectocandidato`
--

DROP TABLE IF EXISTS `persona_aspectocandidato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_aspectocandidato` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `estatus` varchar(140) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_aspectocandidato_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_fe3e07be` FOREIGN KEY (`person_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_aspectocandidato`
--

LOCK TABLES `persona_aspectocandidato` WRITE;
/*!40000 ALTER TABLE `persona_aspectocandidato` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_aspectocandidato` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_aspectohogar`
--

DROP TABLE IF EXISTS `persona_aspectohogar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_aspectohogar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `estatus` varchar(140) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_aspectohogar_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_8f287a74` FOREIGN KEY (`person_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_aspectohogar`
--

LOCK TABLES `persona_aspectohogar` WRITE;
/*!40000 ALTER TABLE `persona_aspectohogar` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_aspectohogar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_automovil`
--

DROP TABLE IF EXISTS `persona_automovil`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_automovil` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `marca` varchar(140) NOT NULL,
  `modelo_ano` varchar(140) NOT NULL,
  `liquidacion` varchar(140) NOT NULL,
  `valor_comercial` varchar(140) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_automovil_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_d72f520d` FOREIGN KEY (`person_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_automovil`
--

LOCK TABLES `persona_automovil` WRITE;
/*!40000 ALTER TABLE `persona_automovil` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_automovil` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_bienesraices`
--

DROP TABLE IF EXISTS `persona_bienesraices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_bienesraices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `tipo_inmueble` varchar(140) NOT NULL,
  `ubicacion` varchar(140) NOT NULL,
  `liquidacion` varchar(140) NOT NULL,
  `valor_comercial` varchar(140) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_bienesraices_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_72b76d87` FOREIGN KEY (`person_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_bienesraices`
--

LOCK TABLES `persona_bienesraices` WRITE;
/*!40000 ALTER TABLE `persona_bienesraices` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_bienesraices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_caractaristicasvivienda`
--

DROP TABLE IF EXISTS `persona_caractaristicasvivienda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_caractaristicasvivienda` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `propia` varchar(50) NOT NULL,
  `rentada` varchar(50) NOT NULL,
  `hipotecada` varchar(50) NOT NULL,
  `prestada` varchar(50) NOT NULL,
  `otra` varchar(50) NOT NULL,
  `valor_aproximado` varchar(50) NOT NULL,
  `renta_mensual` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_caractaristicasvivienda_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_c08f45ca` FOREIGN KEY (`person_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_caractaristicasvivienda`
--

LOCK TABLES `persona_caractaristicasvivienda` WRITE;
/*!40000 ALTER TABLE `persona_caractaristicasvivienda` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_caractaristicasvivienda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_cuadroevaluacion`
--

DROP TABLE IF EXISTS `persona_cuadroevaluacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_cuadroevaluacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `conclusiones` longtext NOT NULL,
  `viable` varchar(140) NOT NULL,
  `no_viable` varchar(140) NOT NULL,
  `reservas` varchar(140) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_cuadroevaluacion_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_76118f1f` FOREIGN KEY (`person_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_cuadroevaluacion`
--

LOCK TABLES `persona_cuadroevaluacion` WRITE;
/*!40000 ALTER TABLE `persona_cuadroevaluacion` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_cuadroevaluacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_cuentadebito`
--

DROP TABLE IF EXISTS `persona_cuentadebito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_cuentadebito` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `institucion` varchar(140) NOT NULL,
  `saldo_mensual` varchar(140) NOT NULL,
  `antiguedad` varchar(140) NOT NULL,
  `ahorro` varchar(140) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_cuentadebito_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_e4423503` FOREIGN KEY (`person_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_cuentadebito`
--

LOCK TABLES `persona_cuentadebito` WRITE;
/*!40000 ALTER TABLE `persona_cuentadebito` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_cuentadebito` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_deudaactual`
--

DROP TABLE IF EXISTS `persona_deudaactual`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_deudaactual` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `fecha_otorgamiento` date DEFAULT NULL,
  `tipo` varchar(140) NOT NULL,
  `institucion` varchar(140) NOT NULL,
  `cantidad_total` varchar(140) NOT NULL,
  `saldo_actual` varchar(140) NOT NULL,
  `pago_mensual` varchar(140) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_deudaactual_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_d134a95a` FOREIGN KEY (`person_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_deudaactual`
--

LOCK TABLES `persona_deudaactual` WRITE;
/*!40000 ALTER TABLE `persona_deudaactual` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_deudaactual` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_direccion`
--

DROP TABLE IF EXISTS `persona_direccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_direccion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persona_id` int(11) NOT NULL,
  `calle` varchar(140) DEFAULT NULL,
  `ciudad` varchar(140) DEFAULT NULL,
  `colonia` varchar(140) DEFAULT NULL,
  `cp` varchar(140) DEFAULT NULL,
  `estado` varchar(140) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_direccion_e27cbd6d` (`persona_id`),
  CONSTRAINT `persona_id_refs_id_b3e6caf3` FOREIGN KEY (`persona_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_direccion`
--

LOCK TABLES `persona_direccion` WRITE;
/*!40000 ALTER TABLE `persona_direccion` DISABLE KEYS */;
INSERT INTO `persona_direccion` VALUES (1,1,'Tijuana, Tijuana','Tijuana','Tijuana','22200','Baja California'),(2,2,'Tijuana, Tijuana','Tijuana','Tijuana','22200','Baja California'),(3,3,'','HERMOSILLO','','','Sonora'),(4,4,'EVEREST','TIJUANA','LA CUSPIDE RESIDENCIAL','22517','Baja California'),(5,5,'a','4','a','1','Baja California');
/*!40000 ALTER TABLE `persona_direccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_distribuciondimensiones`
--

DROP TABLE IF EXISTS `persona_distribuciondimensiones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_distribuciondimensiones` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `habitaciones` varchar(50) NOT NULL,
  `banos` varchar(50) NOT NULL,
  `salas` varchar(50) NOT NULL,
  `comedor` varchar(50) NOT NULL,
  `cocina` varchar(50) NOT NULL,
  `patios` varchar(50) NOT NULL,
  `cocheras` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_distribuciondimensiones_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_6b63946a` FOREIGN KEY (`person_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_distribuciondimensiones`
--

LOCK TABLES `persona_distribuciondimensiones` WRITE;
/*!40000 ALTER TABLE `persona_distribuciondimensiones` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_distribuciondimensiones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_documentocotejado`
--

DROP TABLE IF EXISTS `persona_documentocotejado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_documentocotejado` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `estatus` varchar(140) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_documentocotejado_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_ac428220` FOREIGN KEY (`person_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_documentocotejado`
--

LOCK TABLES `persona_documentocotejado` WRITE;
/*!40000 ALTER TABLE `persona_documentocotejado` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_documentocotejado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_economica`
--

DROP TABLE IF EXISTS `persona_economica`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_economica` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `concepto` varchar(140) NOT NULL,
  `monto` double NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_economica_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_2c69befb` FOREIGN KEY (`person_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_economica`
--

LOCK TABLES `persona_economica` WRITE;
/*!40000 ALTER TABLE `persona_economica` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_economica` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_evaluacion`
--

DROP TABLE IF EXISTS `persona_evaluacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_evaluacion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `trayectoriaLaboral_id` int(11) NOT NULL,
  `productividad` varchar(20) DEFAULT NULL,
  `adaptabilidad` varchar(20) DEFAULT NULL,
  `motivacion` varchar(20) DEFAULT NULL,
  `puntualidad` varchar(20) DEFAULT NULL,
  `asistencia` varchar(20) DEFAULT NULL,
  `disponibilidad` varchar(20) DEFAULT NULL,
  `responsabilidad` varchar(20) DEFAULT NULL,
  `relacion_jefe_inmediato` varchar(20) DEFAULT NULL,
  `relacion_companeros` varchar(20) DEFAULT NULL,
  `compromiso` varchar(20) DEFAULT NULL,
  `honestidad` varchar(20) DEFAULT NULL,
  `toma_decisiones` varchar(20) DEFAULT NULL,
  `solucion_problemas` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_evaluacion_12aafd20` (`trayectoriaLaboral_id`),
  CONSTRAINT `trayectoriaLaboral_id_refs_id_1877e19c` FOREIGN KEY (`trayectoriaLaboral_id`) REFERENCES `persona_trayectorialaboral` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_evaluacion`
--

LOCK TABLES `persona_evaluacion` WRITE;
/*!40000 ALTER TABLE `persona_evaluacion` DISABLE KEYS */;
INSERT INTO `persona_evaluacion` VALUES (1,1,'1','2','4','3','3','3','3','3','3','3','','4','4'),(2,2,'2','2','2','2','2','2','2','2','2','2','2','2','2'),(3,3,'','2','','','','','','','','','','',''),(4,4,'','','','','','','','','','','','',''),(5,5,'','','','','','','','','','','','',''),(6,6,'1','1','1','1','1','1','1','1','1','1','1','1','1'),(7,7,'1','1','1','1','1','1','1','1','1','1','1','1','1');
/*!40000 ALTER TABLE `persona_evaluacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_file`
--

DROP TABLE IF EXISTS `persona_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_file` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `record` varchar(100) NOT NULL,
  `fecha_registro` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_file`
--

LOCK TABLES `persona_file` WRITE;
/*!40000 ALTER TABLE `persona_file` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_file` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_gradoescolaridad`
--

DROP TABLE IF EXISTS `persona_gradoescolaridad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_gradoescolaridad` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `grado` varchar(20) NOT NULL,
  `institucion` varchar(200) NOT NULL,
  `ciudad` varchar(200) NOT NULL,
  `anos` varchar(200) NOT NULL,
  `certificado` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_gradoescolaridad_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_b600ebf4` FOREIGN KEY (`person_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_gradoescolaridad`
--

LOCK TABLES `persona_gradoescolaridad` WRITE;
/*!40000 ALTER TABLE `persona_gradoescolaridad` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_gradoescolaridad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_infopersonal`
--

DROP TABLE IF EXISTS `persona_infopersonal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_infopersonal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persona_id` int(11) NOT NULL,
  `objetivo_personal` varchar(500) NOT NULL,
  `objetivo_en_empresa` varchar(500) NOT NULL,
  `cualidades` varchar(500) NOT NULL,
  `defectos` varchar(500) NOT NULL,
  `trabajo_que_desarrolla` varchar(500) NOT NULL,
  `tatuajes` varchar(500) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_infopersonal_e27cbd6d` (`persona_id`),
  CONSTRAINT `persona_id_refs_id_136087d2` FOREIGN KEY (`persona_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_infopersonal`
--

LOCK TABLES `persona_infopersonal` WRITE;
/*!40000 ALTER TABLE `persona_infopersonal` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_infopersonal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_informante`
--

DROP TABLE IF EXISTS `persona_informante`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_informante` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `evaluacion_id` int(11) NOT NULL,
  `nombre` varchar(140) DEFAULT NULL,
  `puesto` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_informante_20f35463` (`evaluacion_id`),
  CONSTRAINT `evaluacion_id_refs_id_a20b31e9` FOREIGN KEY (`evaluacion_id`) REFERENCES `persona_evaluacion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_informante`
--

LOCK TABLES `persona_informante` WRITE;
/*!40000 ALTER TABLE `persona_informante` DISABLE KEYS */;
INSERT INTO `persona_informante` VALUES (1,1,'DSAD','ASDASD'),(2,2,'FABIAN ALDAMA','COORDINADOR RH'),(3,3,'JOSÉ LUIS MENDOZA','ADMINISTRADOR'),(4,4,'MARIA VAZQUEZ','AUXILIAR DE RECURSOS HUMANOS'),(5,5,'MARIBEL MORALES','ASISTENTE DE RECURSOS HUMANOS'),(6,6,'LORENA NÚÑEZ MANQUERO','SUBGERENTE DE CAPITAL HUMANOS'),(7,7,'fghfgh','fghfgh'),(8,7,'fghfgh','fghfgh');
/*!40000 ALTER TABLE `persona_informante` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_legalidad`
--

DROP TABLE IF EXISTS `persona_legalidad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_legalidad` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persona_id` int(11) NOT NULL,
  `sindicato` varchar(500) DEFAULT NULL,
  `afiliado_sindicato` int(11) NOT NULL,
  `demandas` int(11) NOT NULL,
  `antecedentes_penales` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_legalidad_e27cbd6d` (`persona_id`),
  CONSTRAINT `persona_id_refs_id_5594ea6` FOREIGN KEY (`persona_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_legalidad`
--

LOCK TABLES `persona_legalidad` WRITE;
/*!40000 ALTER TABLE `persona_legalidad` DISABLE KEYS */;
INSERT INTO `persona_legalidad` VALUES (1,1,'',0,0,0),(2,2,'',0,0,0),(3,3,'',2,2,2),(4,4,'',2,2,2),(5,5,'4',1,1,1);
/*!40000 ALTER TABLE `persona_legalidad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_licencia`
--

DROP TABLE IF EXISTS `persona_licencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_licencia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persona_id` int(11) NOT NULL,
  `numero` varchar(20) NOT NULL,
  `tipo` varchar(14) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_licencia_e27cbd6d` (`persona_id`),
  CONSTRAINT `persona_id_refs_id_73bfb654` FOREIGN KEY (`persona_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_licencia`
--

LOCK TABLES `persona_licencia` WRITE;
/*!40000 ALTER TABLE `persona_licencia` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_licencia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_miembromarcofamiliar`
--

DROP TABLE IF EXISTS `persona_miembromarcofamiliar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_miembromarcofamiliar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `nombre` varchar(140) NOT NULL,
  `edad` varchar(140) DEFAULT NULL,
  `ocupacion` varchar(140) DEFAULT NULL,
  `empresa` varchar(140) DEFAULT NULL,
  `residencia` varchar(140) DEFAULT NULL,
  `telefono` varchar(140) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_miembromarcofamiliar_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_5431d858` FOREIGN KEY (`person_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_miembromarcofamiliar`
--

LOCK TABLES `persona_miembromarcofamiliar` WRITE;
/*!40000 ALTER TABLE `persona_miembromarcofamiliar` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_miembromarcofamiliar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_opinion`
--

DROP TABLE IF EXISTS `persona_opinion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_opinion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `evaluacion_id` int(11) NOT NULL,
  `categoria` varchar(20) NOT NULL,
  `opinion` longtext,
  PRIMARY KEY (`id`),
  KEY `persona_opinion_20f35463` (`evaluacion_id`),
  CONSTRAINT `evaluacion_id_refs_id_7e30cd09` FOREIGN KEY (`evaluacion_id`) REFERENCES `persona_evaluacion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_opinion`
--

LOCK TABLES `persona_opinion` WRITE;
/*!40000 ALTER TABLE `persona_opinion` DISABLE KEYS */;
INSERT INTO `persona_opinion` VALUES (1,1,'1','kjsdhnasm,d '),(2,2,'1','NO SE OBTUVO INFORMACIÓN DEL JEFE INMEDIATO'),(3,2,'2','NO TUVO INCIDENCIAS DURANTE SU DESEMPEÑO EN LA EMPRESA'),(4,3,'2','SIN INCIDENCIAS DURANTE SU PARTICIPACIÓN EN LA EMPRESA'),(5,4,'2','SIN INCIDENCIAS REGISTRADA EN SISTEMA.'),(6,5,'2','SIN INCIDENCIAS REGISTRADAS EN EL SISTEMA. DE ACUERDO A SU KARDEX, FUE CONSTANTE DE PRINCIPIO A FIN.'),(7,6,'2','SIN INCIDENCIAS DURANTE SU DESEMPEÑO EN LA EMPRESA'),(8,7,'1','nnfnfgn'),(9,7,'2','fghfghfg');
/*!40000 ALTER TABLE `persona_opinion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_origen`
--

DROP TABLE IF EXISTS `persona_origen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_origen` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persona_id` int(11) NOT NULL,
  `lugar` varchar(140) DEFAULT NULL,
  `nacionalidad` varchar(140) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_origen_e27cbd6d` (`persona_id`),
  CONSTRAINT `persona_id_refs_id_fda675e` FOREIGN KEY (`persona_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_origen`
--

LOCK TABLES `persona_origen` WRITE;
/*!40000 ALTER TABLE `persona_origen` DISABLE KEYS */;
INSERT INTO `persona_origen` VALUES (1,1,'','',NULL),(2,2,'','',NULL),(3,3,'SONORA','MEXICANA','1988-03-03'),(4,4,'GUASAVE, SINALOA','MEXICANA','1995-12-26'),(5,5,'m','m','2017-08-14');
/*!40000 ALTER TABLE `persona_origen` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_otroidioma`
--

DROP TABLE IF EXISTS `persona_otroidioma`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_otroidioma` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `porcentaje` int(11) NOT NULL,
  `idioma` varchar(140) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_otroidioma_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_5ae73a45` FOREIGN KEY (`person_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_otroidioma`
--

LOCK TABLES `persona_otroidioma` WRITE;
/*!40000 ALTER TABLE `persona_otroidioma` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_otroidioma` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_persona`
--

DROP TABLE IF EXISTS `persona_persona`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_persona` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(140) NOT NULL,
  `nss` varchar(30) DEFAULT NULL,
  `email` varchar(140) DEFAULT NULL,
  `edad` int(11) DEFAULT NULL,
  `curp` varchar(30) DEFAULT NULL,
  `malos_terminos` int(11) DEFAULT NULL,
  `rfc` varchar(30) DEFAULT NULL,
  `ife` varchar(30) DEFAULT NULL,
  `pasaporte` varchar(30) DEFAULT NULL,
  `smn` varchar(30) DEFAULT NULL,
  `estado_civil` int(11) DEFAULT NULL,
  `fecha_matrimonio` date DEFAULT NULL,
  `religion` varchar(140) DEFAULT NULL,
  `tiempo_radicando` varchar(140) DEFAULT NULL,
  `medio_utilizado` varchar(140) DEFAULT NULL,
  `fecha_registro` date NOT NULL,
  `estatus` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_persona`
--

LOCK TABLES `persona_persona` WRITE;
/*!40000 ALTER TABLE `persona_persona` DISABLE KEYS */;
INSERT INTO `persona_persona` VALUES (1,'Fernanda','11111111111','fernanda@contakto.mx',NULL,'',0,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,'2019-01-23',1),(2,'Fernanda','123','fernanda@contakto.mx',NULL,'',0,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,'2019-01-23',1),(3,'DOMINGO ANTONIO CASILLAS BARRAGAN','24028801595','anitha.ajgn@gmail.com',30,'CABD880327HSRSRM01',2,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,'2019-01-29',1),(4,'ARAEL FERNANDA ANGULO ATONDO','03169556689','arael.fernanda@gmail.com',23,'AUAA951226MSLNTR00',2,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,'2019-02-05',1),(5,'Juan Carlos Vargas Cordero','123456987451351321521351513215','',NULL,'',1,NULL,NULL,NULL,NULL,0,NULL,NULL,NULL,NULL,'2019-02-05',1);
/*!40000 ALTER TABLE `persona_persona` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_prestacionvivienda`
--

DROP TABLE IF EXISTS `persona_prestacionvivienda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_prestacionvivienda` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persona_id` int(11) NOT NULL,
  `categoria_viv` varchar(20) NOT NULL,
  `activo` int(11) DEFAULT NULL,
  `fecha_tramite` date DEFAULT NULL,
  `numero_credito` varchar(140) DEFAULT NULL,
  `uso` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_prestacionvivienda_e27cbd6d` (`persona_id`),
  CONSTRAINT `persona_id_refs_id_a9349c8c` FOREIGN KEY (`persona_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_prestacionvivienda`
--

LOCK TABLES `persona_prestacionvivienda` WRITE;
/*!40000 ALTER TABLE `persona_prestacionvivienda` DISABLE KEYS */;
INSERT INTO `persona_prestacionvivienda` VALUES (1,1,'infonavit',0,NULL,'',NULL),(2,1,'fonacot',0,NULL,'',NULL),(3,2,'infonavit',0,NULL,'',NULL),(4,2,'fonacot',0,NULL,'',NULL),(5,3,'infonavit',2,NULL,'',NULL),(6,3,'fonacot',2,NULL,'',NULL),(7,4,'infonavit',2,NULL,'',NULL),(8,4,'fonacot',2,NULL,'',NULL),(9,5,'infonavit',1,NULL,'5',NULL),(10,5,'fonacot',1,NULL,'4',NULL);
/*!40000 ALTER TABLE `persona_prestacionvivienda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_propietariovivienda`
--

DROP TABLE IF EXISTS `persona_propietariovivienda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_propietariovivienda` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `parentesco` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_propietariovivienda_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_e5e6c7ab` FOREIGN KEY (`person_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_propietariovivienda`
--

LOCK TABLES `persona_propietariovivienda` WRITE;
/*!40000 ALTER TABLE `persona_propietariovivienda` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_propietariovivienda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_referencia`
--

DROP TABLE IF EXISTS `persona_referencia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_referencia` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `nombre` varchar(140) NOT NULL,
  `domicilio` varchar(200) NOT NULL,
  `telefono` varchar(140) NOT NULL,
  `tiempo_conocido` varchar(140) NOT NULL,
  `parentesco` varchar(140) NOT NULL,
  `ocupacion` varchar(140) NOT NULL,
  `lugares_labor_evaluado` varchar(200) NOT NULL,
  `opinion` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_referencia_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_f1855cf8` FOREIGN KEY (`person_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_referencia`
--

LOCK TABLES `persona_referencia` WRITE;
/*!40000 ALTER TABLE `persona_referencia` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_referencia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_salud`
--

DROP TABLE IF EXISTS `persona_salud`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_salud` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persona_id` int(11) NOT NULL,
  `peso_kg` double NOT NULL,
  `estatura_mts` double NOT NULL,
  `salud_fisica` varchar(200) NOT NULL,
  `salud_visual` varchar(200) NOT NULL,
  `embarazo_meses` varchar(200) NOT NULL,
  `ejercicio_tipo_frecuencia` varchar(200) NOT NULL,
  `accidentes` varchar(200) NOT NULL,
  `intervenciones_quirurgicas` varchar(200) NOT NULL,
  `enfermedades_familiares` varchar(200) NOT NULL,
  `tratamiento_medico_psicologico` varchar(200) NOT NULL,
  `enfermedades_mayor_frecuencia` varchar(200) NOT NULL,
  `institucion_medica` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_salud_e27cbd6d` (`persona_id`),
  CONSTRAINT `persona_id_refs_id_c66dd286` FOREIGN KEY (`persona_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_salud`
--

LOCK TABLES `persona_salud` WRITE;
/*!40000 ALTER TABLE `persona_salud` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_salud` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_seguro`
--

DROP TABLE IF EXISTS `persona_seguro`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_seguro` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persona_id` int(11) NOT NULL,
  `ultimas_aportaciones` int(11) NOT NULL,
  `verificado_enburo` int(11) NOT NULL,
  `registro_completo` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_seguro_e27cbd6d` (`persona_id`),
  CONSTRAINT `persona_id_refs_id_775ae547` FOREIGN KEY (`persona_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_seguro`
--

LOCK TABLES `persona_seguro` WRITE;
/*!40000 ALTER TABLE `persona_seguro` DISABLE KEYS */;
INSERT INTO `persona_seguro` VALUES (1,1,0,0,0),(2,2,0,0,0),(3,3,2,1,1),(4,4,2,1,1),(5,5,1,1,1);
/*!40000 ALTER TABLE `persona_seguro` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_situacionvivienda`
--

DROP TABLE IF EXISTS `persona_situacionvivienda`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_situacionvivienda` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `tiempo_radicando` varchar(50) NOT NULL,
  `tipo_mobiliario` varchar(200) NOT NULL,
  `sector_socioeconomico` varchar(200) NOT NULL,
  `personas_viven_con_evaluado` varchar(50) NOT NULL,
  `conservacion` varchar(200) NOT NULL,
  `tamano_aprox_mts2` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_situacionvivienda_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_d3205250` FOREIGN KEY (`person_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_situacionvivienda`
--

LOCK TABLES `persona_situacionvivienda` WRITE;
/*!40000 ALTER TABLE `persona_situacionvivienda` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_situacionvivienda` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_tarjetacreditocomercial`
--

DROP TABLE IF EXISTS `persona_tarjetacreditocomercial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_tarjetacreditocomercial` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `institucion` varchar(140) NOT NULL,
  `limite_credito` varchar(140) NOT NULL,
  `pago_minimo` varchar(140) NOT NULL,
  `saldo_actual` varchar(140) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_tarjetacreditocomercial_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_a37113b1` FOREIGN KEY (`person_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_tarjetacreditocomercial`
--

LOCK TABLES `persona_tarjetacreditocomercial` WRITE;
/*!40000 ALTER TABLE `persona_tarjetacreditocomercial` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_tarjetacreditocomercial` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_telefono`
--

DROP TABLE IF EXISTS `persona_telefono`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_telefono` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persona_id` int(11) NOT NULL,
  `categoria` varchar(20) NOT NULL,
  `numero` varchar(14) DEFAULT NULL,
  `parentesco` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_telefono_e27cbd6d` (`persona_id`),
  CONSTRAINT `persona_id_refs_id_1d09cbba` FOREIGN KEY (`persona_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_telefono`
--

LOCK TABLES `persona_telefono` WRITE;
/*!40000 ALTER TABLE `persona_telefono` DISABLE KEYS */;
INSERT INTO `persona_telefono` VALUES (1,1,'casa','016871034188',NULL),(2,1,'movil','',NULL),(3,1,'recado','',NULL),(4,2,'casa','016871034188',NULL),(5,2,'movil','',NULL),(6,2,'recado','',NULL),(7,3,'casa','',NULL),(8,3,'movil','(662) 374-3557',NULL),(9,3,'recado','(662) 426-9189',NULL),(10,4,'casa','',NULL),(11,4,'movil','(687) 103-4188',NULL),(12,4,'recado','',NULL),(13,5,'casa','(2',NULL),(14,5,'movil','(3',NULL),(15,5,'recado','(4',NULL);
/*!40000 ALTER TABLE `persona_telefono` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_tipoinmueble`
--

DROP TABLE IF EXISTS `persona_tipoinmueble`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_tipoinmueble` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `person_id` int(11) NOT NULL,
  `casa` varchar(50) NOT NULL,
  `terreno_compartido` varchar(50) NOT NULL,
  `departamento` varchar(50) NOT NULL,
  `vivienda_popular` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_tipoinmueble_21b911c5` (`person_id`),
  CONSTRAINT `person_id_refs_id_ca6b963` FOREIGN KEY (`person_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_tipoinmueble`
--

LOCK TABLES `persona_tipoinmueble` WRITE;
/*!40000 ALTER TABLE `persona_tipoinmueble` DISABLE KEYS */;
/*!40000 ALTER TABLE `persona_tipoinmueble` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persona_trayectorialaboral`
--

DROP TABLE IF EXISTS `persona_trayectorialaboral`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persona_trayectorialaboral` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `persona_id` int(11) NOT NULL,
  `compania_id` int(11) NOT NULL,
  `aparece_nss` int(11) NOT NULL,
  `aportaciones_fecha_inicial` date DEFAULT NULL,
  `aportaciones_fecha_final` date DEFAULT NULL,
  `reporta_candidato` int(11) NOT NULL,
  `carta_laboral` int(11) NOT NULL,
  `carta_laboral_expide` varchar(140) DEFAULT NULL,
  `puesto_inicial` varchar(140) DEFAULT NULL,
  `puesto_final` varchar(140) DEFAULT NULL,
  `periodo_alta` varchar(140) DEFAULT NULL,
  `periodo_baja` varchar(140) DEFAULT NULL,
  `sueldo_inicial` varchar(140) DEFAULT NULL,
  `sueldo_final` varchar(140) DEFAULT NULL,
  `funciones` longtext,
  `cumplio_objetivos` longtext,
  `motivo_salida` varchar(140) DEFAULT NULL,
  `jefe_inmediato` varchar(140) DEFAULT NULL,
  `jefe_inmediato_puesto` varchar(140) DEFAULT NULL,
  `no_personas_cargo` varchar(140) DEFAULT NULL,
  `manejo_valores` int(11) NOT NULL,
  `recontratable` varchar(140) DEFAULT NULL,
  `afiliado_sindicato` int(11) NOT NULL,
  `terminada` tinyint(1) NOT NULL,
  `visible_en_status` tinyint(1) NOT NULL,
  `observaciones_generales` longtext,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `persona_trayectorialaboral_e27cbd6d` (`persona_id`),
  KEY `persona_trayectorialaboral_2a71e362` (`compania_id`),
  CONSTRAINT `compania_id_refs_id_3b0fe8ca` FOREIGN KEY (`compania_id`) REFERENCES `compania_compania` (`id`),
  CONSTRAINT `persona_id_refs_id_58422c36` FOREIGN KEY (`persona_id`) REFERENCES `persona_persona` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persona_trayectorialaboral`
--

LOCK TABLES `persona_trayectorialaboral` WRITE;
/*!40000 ALTER TABLE `persona_trayectorialaboral` DISABLE KEYS */;
INSERT INTO `persona_trayectorialaboral` VALUES (1,2,1,0,NULL,NULL,0,0,'','leroelro','lerolero','03/10/2018','23/01/2019','$12.00','$12.00','','NO','1','','','0',0,'NO',0,1,1,'jjjjjjjjjjjjjjjjjj',1),(2,3,2,1,NULL,NULL,1,2,'','GUARDIA DE SEGURIDAD','GUARDIA DE SEGURIDAD','11/04/2018','28/09/2018','CONFIDENCIAL','CONFIDENCIAL','','SI','0','ALEXANDER ARIAS','SUPERVISOR DE GUARDIAS','0',2,'SI',2,0,1,'NO SE ENCONTRARON INCIDENCIAS PARA OBTENER LA REFERENCIA DEL CANDIDATO.',1),(3,3,4,0,NULL,NULL,1,2,'','AYUDANTE DE ALBAÑIL','AYUDANTE DE ALBAÑIL','25/09/2017','11/04/2018','CONFIDENCIAL','CONFIDENCIAL','','','3','JOSÉ ALONSO CHOMINA','','0',2,'',2,0,1,'DEBIDO AL CORTO PERIODO DE PARTICIPACIÓN, NO PODÍAN PROPORCIONAR MÁS INFORMACIÓN.',1),(4,3,5,0,NULL,NULL,1,2,'','AUXILIAR DE MANTENIMIENTO','AUXILIAR DE MANTENIMIENTO','12/01/2016','28/07/2016','CONFIDENCIAL','CONFIDENCIAL','','',NULL,'','','0',2,'',0,0,1,'EL CANDIDATO FUE UN REINGRESO EN LA EMPRESA. SU PRIMER COLABORACIÓN FUE DEL 14/05/0215 AL 10/09/2015.',1),(5,3,6,1,NULL,NULL,1,2,'','AYUDANTE DE PERFORISTA','AYUDANTE DE PERFORISTA','01/02/2010','01/10/2010','CONFIDENCIAL','CONFIDENCIAL','','','3','','','0',2,'',2,1,1,'NO SE PRESENTARON DIFICULTADES PARA OBTENER LA REFERENCIA.',1),(6,4,8,2,NULL,NULL,1,1,'LORENA NUÑEZ / SUBGERENTE DE CAPITAL HUMANO','PRACTICANTE','PRACTICANTE','19/09/2017','04/05/2018','CONFIDENCIAL','CONFIDENCIAL','AUXILIAR DE RECURSOS HUMANOS, PRENOMINA, ACTIVIDADES MOTIVACIONALES, CONTROL DE EXPEDIENTES DE COLABORADORES, ETC.','SI','3','YOMARA RODRIGUEZ','ENCARGADA DE PERSONAL','0',2,'SI',2,1,1,'SIN OBSERVACIONES GENERALES.',1),(7,5,7,1,'2019-12-02','2019-12-02',1,1,'asdasdsad','aa','aaa','sss','sss','aaa','aaa','asdasdas','asdasdas','2','nn','nnn','asdasd',1,'no',1,1,1,'fghfgh',1);
/*!40000 ALTER TABLE `persona_trayectorialaboral` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `south_migrationhistory`
--

DROP TABLE IF EXISTS `south_migrationhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `south_migrationhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(255) NOT NULL,
  `migration` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `south_migrationhistory`
--

LOCK TABLES `south_migrationhistory` WRITE;
/*!40000 ALTER TABLE `south_migrationhistory` DISABLE KEYS */;
INSERT INTO `south_migrationhistory` VALUES (1,'agente','0001_initial','2019-01-18 23:20:44'),(2,'bitacora','0001_initial','2019-01-18 23:20:44'),(3,'compania','0001_initial','2019-01-18 23:20:44'),(4,'investigacion','0001_initial','2019-01-18 23:20:45'),(5,'persona','0001_initial','2019-01-18 23:20:50'),(6,'entrevista','0001_initial','2019-01-18 23:20:57'),(7,'cobranza','0001_initial','2019-01-18 23:21:00'),(8,'adjuntos','0001_initial','2019-01-18 23:21:00');
/*!40000 ALTER TABLE `south_migrationhistory` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-02-09 21:40:43
