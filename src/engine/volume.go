package engine

import (
	"time"
)

//
// Volume Datatype
//
type Volume struct {

	Label string  // Volume Label
	LastSnapshot *Snapshot  // Pointer to the most recent snapshot

	Id   string         // Volume ID

	SnapshotInterval time.Duration // Time between snapshots
	SnapshotRetention time.Duration // Time to retain snapshots

	Snapshots []Snapshot              // All the volume snapshots
}

//
// Get the time at which the next snapshot is due
//
func (vol *Volume) NextSnapshotAt() time.Time {

	last_snapshot_time := vol.LastSnapshot.CreatedAt

	return last_snapshot_time.Add(vol.SnapshotInterval)
}

//
// Create a new Volume
//
func NewVolume(
	id string, // Volume ID
	snapshot_interval time.Duration, // Snapshot Interval
	snapshot_retention time.Duration, // Stanpshot Retention Period
) *Volume {
	
	vol := &Volume{
		Id: id,
		SnapshotInterval: snapshot_interval,
		SnapshotRetention: snapshot_retention,
	}

	return vol
}

//
// Snapshot a Volume
//
func (vol *Volume) CreateSnapshot () {
	snapshot := &Snapshot{
		Label: vol.Label + time.Now().String(),
		Volume: vol,
		CreatedAt: time.Now(),
		Status: "new",
	}
	
	vol.Snapshots = append(vol.Snapshots, *snapshot)
	
}

//
// Stringify Volume
//
func (vol *Volume) String () string {
	str := "Volume: " + vol.Id + "\n  Snapshots:"

	for s := range vol.Snapshots {
		str = str + "\n  - " + vol.Snapshots[s].Label
	}

	str = str + "\n"

	return str
}
