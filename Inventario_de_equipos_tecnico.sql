-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         10.1.9-MariaDB-log - mariadb.org binary distribution
-- SO del servidor:              Win32
-- HeidiSQL Versión:             9.3.0.4984
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- Volcando estructura de base de datos para inventario_de_equipos_tecnologicos
CREATE DATABASE IF NOT EXISTS `inventario_de_equipos_tecnologicos` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `inventario_de_equipos_tecnologicos`;


-- Volcando estructura para tabla inventario_de_equipos_tecnologicos.departamento
CREATE TABLE IF NOT EXISTS `departamento` (
  `id_departamento` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_dep` varchar(50) DEFAULT NULL,
  `tipo_de_trabajo` enum('docentes','administrativo') DEFAULT NULL,
  `encargado` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id_departamento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Volcando datos para la tabla inventario_de_equipos_tecnologicos.departamento: ~0 rows (aproximadamente)
/*!40000 ALTER TABLE `departamento` DISABLE KEYS */;
/*!40000 ALTER TABLE `departamento` ENABLE KEYS */;


-- Volcando estructura para tabla inventario_de_equipos_tecnologicos.inventario
CREATE TABLE IF NOT EXISTS `inventario` (
  `id_equipos` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_pc` varchar(20) DEFAULT NULL,
  `mac_placa` varchar(20) DEFAULT NULL,
  `fuentes_de_poder` varchar(20) DEFAULT NULL,
  `disco_duro` varchar(20) DEFAULT NULL,
  `procesador` varchar(20) DEFAULT NULL,
  `ram` varchar(20) DEFAULT NULL,
  `fecha_ingreso` date DEFAULT NULL,
  `estado` enum('disponible','inactivo','mantenimiento') DEFAULT NULL,
  `departamento_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_equipos`),
  KEY `FK_inventario_departamento` (`departamento_id`),
  CONSTRAINT `FK_inventario_departamento` FOREIGN KEY (`departamento_id`) REFERENCES `departamento` (`id_departamento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Volcando datos para la tabla inventario_de_equipos_tecnologicos.inventario: ~0 rows (aproximadamente)
/*!40000 ALTER TABLE `inventario` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventario` ENABLE KEYS */;


-- Volcando estructura para tabla inventario_de_equipos_tecnologicos.login
CREATE TABLE IF NOT EXISTS `login` (
  `id_usuario` int(11) NOT NULL AUTO_INCREMENT,
  `usuario` varchar(12) DEFAULT NULL,
  `tipo_user` enum('Administrador','Invitado') DEFAULT NULL,
  `contrasena` varchar(16) DEFAULT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- Volcando datos para la tabla inventario_de_equipos_tecnologicos.login: ~2 rows (aproximadamente)
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` (`id_usuario`, `usuario`, `tipo_user`, `contrasena`, `avatar`) VALUES
	(1, 'laion', 'Administrador', '123', 'avatar-male2.png'),
	(2, 'leo', 'Administrador', '123', 'avatar-male2.png');
/*!40000 ALTER TABLE `login` ENABLE KEYS */;


-- Volcando estructura para tabla inventario_de_equipos_tecnologicos.otros
CREATE TABLE IF NOT EXISTS `otros` (
  `idotros` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_otros` enum('tv','videobeam') DEFAULT NULL,
  `fecha_ingreso_otros` date DEFAULT NULL,
  `estado_otros` enum('activo','inactivo','mantenimiento') DEFAULT NULL,
  `descripcion_otros` varchar(50) DEFAULT NULL,
  `idotros_iddepartamento` int(11) DEFAULT NULL,
  PRIMARY KEY (`idotros`),
  KEY `FK_otros_departamento` (`idotros_iddepartamento`),
  CONSTRAINT `FK_otros_departamento` FOREIGN KEY (`idotros_iddepartamento`) REFERENCES `departamento` (`id_departamento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Volcando datos para la tabla inventario_de_equipos_tecnologicos.otros: ~0 rows (aproximadamente)
/*!40000 ALTER TABLE `otros` DISABLE KEYS */;
/*!40000 ALTER TABLE `otros` ENABLE KEYS */;


-- Volcando estructura para tabla inventario_de_equipos_tecnologicos.reporte
CREATE TABLE IF NOT EXISTS `reporte` (
  `id_reporte` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_reporte` varchar(255) NOT NULL,
  `departamento_id` int(11) NOT NULL,
  `fecha_creacion` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `ruta_archivo` varchar(255) NOT NULL,
  `id_usuario` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_reporte`),
  KEY `departamento_id` (`departamento_id`),
  KEY `FK_reporte_login` (`id_usuario`),
  CONSTRAINT `FK_reporte_login` FOREIGN KEY (`id_usuario`) REFERENCES `login` (`id_usuario`),
  CONSTRAINT `reporte_ibfk_1` FOREIGN KEY (`departamento_id`) REFERENCES `departamento` (`id_departamento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Volcando datos para la tabla inventario_de_equipos_tecnologicos.reporte: ~0 rows (aproximadamente)
/*!40000 ALTER TABLE `reporte` DISABLE KEYS */;
/*!40000 ALTER TABLE `reporte` ENABLE KEYS */;


-- Volcando estructura para tabla inventario_de_equipos_tecnologicos.reporte_global
CREATE TABLE IF NOT EXISTS `reporte_global` (
  `id_reporte_global` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_global` varchar(50) DEFAULT NULL,
  `fecha_creacion_global` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `ruta_archivo_global` varchar(50) DEFAULT NULL,
  `id_usuario_global` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_reporte_global`),
  KEY `FK_reporte_global_login` (`id_usuario_global`),
  CONSTRAINT `FK_reporte_global_login` FOREIGN KEY (`id_usuario_global`) REFERENCES `login` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Volcando datos para la tabla inventario_de_equipos_tecnologicos.reporte_global: ~0 rows (aproximadamente)
/*!40000 ALTER TABLE `reporte_global` DISABLE KEYS */;
/*!40000 ALTER TABLE `reporte_global` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
