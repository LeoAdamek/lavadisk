package engine

import (
	"time"
)

//
// Snapshot Datatype
//
type Snapshot struct {
	
	Status string

	CreatedAt time.Time  // When the snapshot was created

	Label string         // Snapshot Label
	Volume *Volume       // Pointer to the volume this snapshot is of
}


func NewSnapshot(
	status string, // Snapshot status
	createdAt time.Time, // Snapshot creation time
	label string,  // Snapshot label
	volume *Volume, // Snapshotted voluem
) *Snapshot {
	
	s := &Snapshot{
		Status: status,
		CreatedAt: createdAt,
		Label: label,
		Volume: volume,
	}

	return s
}


//
// Destory a snapshot
// Will de-register it from the volume it was created from.
//
// @return bool Operation sucess
func (snap *Snapshot) Destroy() bool {
	
	return true

}

//
// Deregister a snapshot from the volume 
//
func (snap *Snapshot) deregister() {
	
}
