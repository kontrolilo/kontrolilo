/*
Copyright © 2025 NAME HERE <EMAIL ADDRESS>
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
		err := configuration.LoadConfiguration()
		if err != nil {
			panic(fmt.Errorf("fatal error config file: %w", err))
		}

		fmt.Println("Your current configuration")
		fmt.Println("allowed licenses:")
		for _, v := range configuration.GetAllowedLicenses() {
			fmt.Printf(" * %s\n", v)
		}
		fmt.Println("excluded packages:")
		for _, v := range configuration.GetExcludedPackages() {
			fmt.Printf(" * %s\n", v)
		}
	},
}

func init() {
	rootCmd.AddCommand(lintCmd)

	// Here you will define your flags and configuration settings.

	// Cobra supports Persistent Flags which will work for this command
	// and all subcommands, e.g.:
	// lintCmd.PersistentFlags().String("foo", "", "A help for foo")

	// Cobra supports local flags which will only run when this command
	// is called directly, e.g.:
	// lintCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
