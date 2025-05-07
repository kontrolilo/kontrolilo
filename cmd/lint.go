/*
Copyright © 2025 Nicolas Byl <nico@nicolas-byl.eu>
*/
package cmd

import (
	"fmt"

	"github.com/kontrolilo/kontrolilo/internal/pkg/configuration"
	"github.com/spf13/cobra"
)

var lintCmd = &cobra.Command{
	Use:   "lint",
	Short: "Check your local configuration file",
	Long:  `This command will try load the configuration file and show it's current configuration.`,
	Run: func(cmd *cobra.Command, args []string) {
		err := configuration.LoadConfiguration(CfgFile)
		if err != nil {
			panic(fmt.Errorf("fatal error config file: %w", err))
		}

		fmt.Println("Your current configuration")
		fmt.Println("* Allowed licenses:")
		for _, v := range configuration.GetAllowedLicenses() {
			fmt.Printf("   * %s\n", v)
		}
		fmt.Println("* Excluded packages:")
		for _, v := range configuration.GetExcludedPackages() {
			fmt.Printf("   * %s\n", v)
		}
	},
}

func init() {
	rootCmd.AddCommand(lintCmd)
}
