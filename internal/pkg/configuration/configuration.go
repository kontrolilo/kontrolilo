package configuration

import "github.com/spf13/viper"

func LoadConfiguration() error {
	viper.SetConfigName(".kontrolilo")
	viper.SetConfigType("yaml")
	viper.AddConfigPath(".")
	return viper.ReadInConfig()
}

func GetAllowedLicenses() []string {
	return viper.GetStringSlice("allowedLicenses")
}

func GetExcludedPackages() []string {
	return viper.GetStringSlice("excludedPackages")
}
