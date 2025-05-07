package configuration

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestLoadConfiguration(t *testing.T) {
	err := LoadConfiguration("../../../test/kontrolilo.yaml")
	assert.Nil(t, err)
	assert.Equal(t, GetAllowedLicenses(), []string{"Apache-2.0", "MIT"})
}
